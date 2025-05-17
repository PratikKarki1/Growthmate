from django.db import migrations

def add_course_categories(apps, schema_editor):
    CourseCategory = apps.get_model('growth_mate_app', 'CourseCategory')
    categories = [
        {'name': 'Business', 'description': 'Business and management courses'},
        {'name': 'Technology', 'description': 'Technology and programming courses'},
        {'name': 'Marketing', 'description': 'Marketing and advertising courses'},
        {'name': 'Finance', 'description': 'Finance and accounting courses'},
        {'name': 'Personal Development', 'description': 'Personal growth and development courses'},
        {'name': 'Health & Wellness', 'description': 'Health and wellness courses'},
        {'name': 'Education', 'description': 'Education and teaching courses'},
        {'name': 'Arts & Design', 'description': 'Arts and design courses'},
    ]
    for category in categories:
        CourseCategory.objects.create(**category)

def remove_course_categories(apps, schema_editor):
    CourseCategory = apps.get_model('growth_mate_app', 'CourseCategory')
    CourseCategory.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('growth_mate_app', '0003_remove_course_rating_remove_course_total_ratings_and_more'),
    ]

    operations = [
        migrations.RunPython(add_course_categories, remove_course_categories),
    ] 