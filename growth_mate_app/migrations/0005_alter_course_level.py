# Generated by Django 4.2.10 on 2025-03-31 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth_mate_app', '0004_alter_enrollment_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20),
        ),
    ]
