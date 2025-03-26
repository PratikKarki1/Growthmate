from django.urls import path
from .views import signup, login_view, logout_view, home, verify_otp, resend_otp, my_courses_view, chat_view, send_message

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('resend-otp/', resend_otp, name='resend_otp'),
    path('my-courses', my_courses_view, name='my_courses'),
    path('chat/', chat_view, name='chat'),
    path('send-message/', send_message, name='send_message'),
]
