from django.contrib import admin
from .models import UserProfile, Course, CourseCategory, CourseTag, CourseReview, CourseProgress, CourseContent, Section, Enrollment, DashboardStats, StudentProgress, Lesson


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'country', 'city')
    list_filter = ('role', 'country', 'city')
    search_fields = ('user__username', 'user__email', 'phone', 'country', 'city')


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1 
    fields = ('heading', 'description', 'images', 'videos')


class CourseContentInline(admin.StackedInline):
    model = CourseContent
    extra = 1 
    fields = ('title', 'description', 'images', 'videos')
    inlines = [SectionInline] 


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'is_active', 'is_featured', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'level')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'instructor', 'thumbnail')
        }),
        ('Course Details', {
            'fields': ('duration', 'level', 'prerequisites', 'objectives', 'target_audience')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured', 'certificate_available', 'max_students')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)
    inlines = [CourseContentInline]


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')


@admin.register(CourseTag)
class CourseTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('course__title', 'user__username', 'comment')


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'completed', 'last_accessed')
    list_filter = ('completed', 'last_accessed')
    search_fields = ('user__username', 'course__title')


@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'description')
    search_fields = ('course__title', 'title', 'description')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('course_content', 'heading', 'description')
    search_fields = ('course_content__title', 'heading', 'description')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'completed', 'completed_at')
    list_filter = ('completed', 'enrolled_at', 'completed_at')
    search_fields = ('user__username', 'course__title')


@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_users', 'total_courses', 'active_courses', 'course_completion_rate')
    list_filter = ('date',)
    search_fields = ('date',)


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress_percentage', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('user__username', 'course__title')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'duration', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('course__title', 'title', 'content')
    ordering = ('course', 'order')