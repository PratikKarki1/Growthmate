from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Retail Manager'),
        ('employee', 'Retail Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    profile_pic = models.ImageField(upload_to='static/profile_images/', blank=True, default='static/assets/images/defaultuser.png')    
    cover_pic = models.ImageField(upload_to='static/cover_images/', blank=True, default='static/assets/images/default_cover.png')    
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    professional_headline = models.CharField(max_length=255, blank=True, null=True) 
    bio = models.TextField(blank=True, null=True)

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


class Course(models.Model):
    image = models.ImageField(upload_to='static/course_images/', blank=True, default='static/assets/images/default_course.png')  
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=50) 
    due_date = models.DateField()
    about_this_course = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CourseContent(models.Model):
    course = models.ForeignKey(Course, related_name="contents", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='static/course_content/images/', blank=True, null=True)
    videos = models.FileField(upload_to='static/course_content/videos/', blank=True, null=True) 

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Section(models.Model):
    course_content = models.ForeignKey(CourseContent, related_name="sections", on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 
    images = models.ImageField(upload_to='static/course_media/images/', blank=True, null=True) 
    videos = models.FileField(upload_to='static/course_media/videos/', blank=True, null=True) 

    def __str__(self):
        return self.heading


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.message[:50]}..."