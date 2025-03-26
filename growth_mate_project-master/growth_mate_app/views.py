from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import random
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Course, UserProfile, ChatMessage
from .tokens import generate_token  
from growth_mate_project import settings 
from django.http import JsonResponse
from django.core.mail import send_mail
import random
from .gemini_service import get_bot_response


otp_storage = {}

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        role = request.POST.get("role") 
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if role not in ["manager", "employee"]:
            messages.error(request, "Invalid role selection.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered, try another email.")
            return redirect("signup")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp  

        email_subject = "Your OTP for Email Verification"
        email_message = f"Hello {first_name},\n\nYour One-Time Password (OTP) for verification is: {otp}\n\nEnter this OTP on the website to activate your account.\n\nThank you!"
        send_mail(email_subject, email_message, settings.EMAIL_HOST_USER, [email], fail_silently=True)

        request.session['temp_user_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password1,
            'role': role
        }

        messages.success(request, "An OTP has been sent to your email. Please enter it to verify your account.")
        return redirect("verify_otp")

    return render(request, "signup.html")

def home(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, "Invalid login credentials, please try again.")
            return redirect("login")

        login(request, user)
        messages.success(request, "Login successful!")
        return redirect("home") 

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

def verify_otp(request):
    if request.method == "POST":
        email = request.session.get('temp_user_data', {}).get('email')
        entered_otp = request.POST.get("otp")

        if not email or email not in otp_storage:
            messages.error(request, "Session expired. Please register again.")
            return redirect("signup")

        if otp_storage[email] == entered_otp:
            user_data = request.session.get('temp_user_data')

            user = User.objects.create_user(username=email, email=email, password=user_data['password'])
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.is_active = True 
            user.save()

            UserProfile.objects.create(user=user, role=user_data['role'])

            del otp_storage[email]
            request.session.pop('temp_user_data', None)

            messages.success(request, "Your account has been activated! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")

    return render(request, "verify_otp.html")


def resend_otp(request):
    if request.method == "POST":
        new_otp = random.randint(100000, 999999)  

        request.session['otp'] = new_otp  

        send_mail(
            "Your New OTP",
            f"Your OTP code is: {new_otp}",
            "no-reply@growthmate.com",
            [request.user.email], 
            fail_silently=False,
        )

        return JsonResponse({"message": "OTP has been resent!", "success": True})
    return JsonResponse({"message": "Invalid request", "success": False}, status=400)

def my_courses_view(request):
    trending_courses = Course.objects.all().order_by('-due_date')[:6]
    return render(request, "my_courses.html", {"trending_courses": trending_courses})

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chat.html', {'messages': messages})

def send_message(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Save user message
        user_message = ChatMessage.objects.create(
            user=request.user,
            message=message,
            is_bot=False
        )
        
        # Get chat history
        chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')[:5]
        
        # Get bot response
        bot_response = get_bot_response(message, chat_history)
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            user=request.user,
            message=bot_response,
            is_bot=True
        )
        
        return JsonResponse({
            'user_message': {
                'message': user_message.message,
                'timestamp': user_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            },
            'bot_message': {
                'message': bot_message.message,
                'timestamp': bot_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)