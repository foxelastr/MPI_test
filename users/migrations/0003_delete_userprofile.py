# Generated by Django 5.0.2 on 2024-03-27 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_student_user_profile'),
        ('users', '0002_alter_userprofile_affiliation_delete_affiliation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
