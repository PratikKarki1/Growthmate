from django.contrib import admin
from .models import UserProfile, Course, CourseContent, Section
from django.db import models


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'role', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('role', 'gender')



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
    list_display = ('title', 'duration', 'due_date', 'uploaded_by')
    search_fields = ('title', 'uploaded_by__username')
    list_filter = ('due_date',)
    ordering = ('-due_date',)
    inlines = [CourseContentInline]  


@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'course')
    search_fields = ('title', 'course__title')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('heading', 'course_content')
    search_fields = ('heading', 'course_content__title')