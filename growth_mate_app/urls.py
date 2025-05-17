from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# URL patterns for the growth_mate_app
urlpatterns = [
    # Home and Authentication Routes
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('select-role/', views.select_role, name='select_role'),

    # Manager Dashboard and Management Routes
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/users/', views.users_view, name='manager_users'),
    path('manager/courses/', views.manager_courses, name='manager_courses'),
    path('manager/available-courses/', views.manager_available_courses, name='manager_available_courses'),
    path('manager/courses/add/', views.add_course, name='add_course'),
    path('manager/courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('manager/courses/<int:course_id>/lessons/', views.manage_lessons, name='manage_lessons'),
    path('manager/courses/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('manager/courses/<int:course_id>/lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('manager/courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('manager/courses/<int:course_id>/', views.view_course, name='view_course'),
    path('manager/courses/form/<int:course_id>/', views.course_form, name='course_form'),
    path('manager/courses/form/', views.course_form, name='course_form'),

    # Profile Settings Route
    path('profile/settings/', views.profile_settings, name='profile_settings'),

    # Employee Dashboard Route
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('available-courses/', views.available_courses, name='available_courses'),
    path('enroll-course/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/details/', views.course_details, name='course_details'),
    path('courses/<int:course_id>/continue/', views.continue_course, name='continue_course'),
    path('lessons/<int:lesson_id>/', views.view_lesson, name='view_lesson'),
    path('users/', views.users_view, name='users'),
    path('users/export/', views.export_users, name='export_users'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),

    # Admin Dashboard Routes - IMPORTANT: These must come before the catch-all pattern
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/add/', views.add_user, name='add_user'),
    path('admin/users/<int:user_id>/update-role/', views.update_user_role, name='update_user_role'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('admin/courses/', views.admin_courses, name='admin_courses'),
    path('admin/courses/add/', views.admin_course_form, name='admin_course_form'),
    path('admin/courses/<int:course_id>/edit/', views.admin_course_form, name='admin_course_form_edit'),
    path('admin/courses/<int:course_id>/lessons/', views.manage_lessons, name='admin_manage_lessons'),
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),

    path('contact/', views.contact_us, name='contact_us'),


    #chatbot route
    path('chat/', views.chat_view, name='chat'),
    path('send-message/', views.send_message, name='send_message'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)