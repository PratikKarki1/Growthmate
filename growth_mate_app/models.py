from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import ImageField, delete
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Retail Manager'),
        ('employee', 'Retail Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    profile_picture = ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    cover_image = ImageField(
        upload_to='cover_images/',
        blank=True,
        null=True
    )
    professional_headline = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

    def get_initials(self):
        """Return the user's initials based on their first and last name."""
        first_name = self.user.first_name or ""
        last_name = self.user.last_name or ""
        
        if first_name and last_name:
            return f"{first_name[0]}{last_name[0]}".upper()
        elif first_name:
            return first_name[0].upper()
        elif last_name:
            return last_name[0].upper()
        else:
            # If no name is available, use the first letter of the email
            return self.user.email[0].upper() if self.user.email else "U"

    def get_full_name(self):
        """Return the user's full name."""
        first_name = self.user.first_name or ""
        last_name = self.user.last_name or ""
        
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        else:
            # If no name is available, use the email
            return self.user.email.split('@')[0] if self.user.email else "Unknown User"

    def save(self, *args, **kwargs):
        # Delete old profile picture if it exists and is being updated
        if self.pk:
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
                if old_instance.profile_picture and self.profile_picture != old_instance.profile_picture:
                    old_instance.profile_picture.delete(save=False)
                if old_instance.cover_image and self.cover_image != old_instance.cover_image:
                    old_instance.cover_image.delete(save=False)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete files when the profile is deleted
        if self.profile_picture:
            self.profile_picture.delete(save=False)
        if self.cover_image:
            self.cover_image.delete(save=False)
        super().delete(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # If user is a superuser, set role as admin
        role = 'admin' if instance.is_superuser else 'employee'
        UserProfile.objects.create(user=instance, role=role)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'userprofile'):
        # If user is a superuser, set role as admin
        role = 'admin' if instance.is_superuser else 'employee'
        UserProfile.objects.create(user=instance, role=role)
    instance.userprofile.save()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey('CourseCategory', on_delete=models.CASCADE, null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", null=True, blank=True)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')
    prerequisites = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    target_audience = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    certificate_available = models.BooleanField(default=False)
    max_students = models.IntegerField(null=True, blank=True)
    enrolled_students = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def active_enrollments(self):
        return self.enrollments.filter(completed=False).count()

    @property
    def completion_rate(self):
        total = self.enrollments.count()
        if total == 0:
            return 0
        completed = self.enrollments.filter(completed=True).count()
        return round((completed / total) * 100, 1)

    @property
    def rating(self):
        return 4.5  # Placeholder for now

    @property
    def total_ratings(self):
        return 120  # Placeholder for now

class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For storing icon class names
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Course Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class CourseTag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['course', 'user']

    def __str__(self):
        return f"{self.user.username}'s review for {self.course.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update course rating
        course = self.course
        reviews = course.reviews.all()
        total_ratings = reviews.count()
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        course.rating = round(avg_rating, 2)
        course.total_ratings = total_ratings
        course.save()

class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField('Lesson')
    last_accessed = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username}'s progress in {self.course.title}"

    @property
    def progress_percentage(self):
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            return 0
        completed_count = self.completed_lessons.count()
        return round((completed_count / total_lessons) * 100, 2)

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

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


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)  # Store progress as percentage
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

class DashboardStats(models.Model):
    date = models.DateField(unique=True)
    total_users = models.IntegerField(default=0)
    total_courses = models.IntegerField(default=0)
    active_courses = models.IntegerField(default=0)
    course_completion_rate = models.FloatField(default=0)
    user_growth_rate = models.FloatField(default=0)
    course_growth_rate = models.FloatField(default=0)
    completion_growth_rate = models.FloatField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Stats for {self.date}"

class StudentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-progress_percentage']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.title} - {self.progress_percentage}%"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    duration = models.IntegerField(help_text='Duration in minutes')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class ContentBlock(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='content_blocks')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='lesson_content/%Y/%m/%d/', blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Content Block'
        verbose_name_plural = 'Content Blocks'

    def __str__(self):
        return f"{self.get_content_type_display()} - {self.lesson.title}"

    def save(self, *args, **kwargs):
        # Delete old file if it exists and is being updated
        if self.pk:
            try:
                old_instance = ContentBlock.objects.get(pk=self.pk)
                if old_instance.file and self.file != old_instance.file:
                    old_instance.file.delete(save=False)
            except ContentBlock.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete file when the content block is deleted
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.description[:50]}"
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.message[:50]}..."