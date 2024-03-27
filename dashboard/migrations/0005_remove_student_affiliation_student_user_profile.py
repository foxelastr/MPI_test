# Generated by Django 5.0.2 on 2024-03-27 04:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_student_affiliation'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='affiliation',
        ),
        migrations.AddField(
            model_name='student',
            name='user_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='users.userprofile', verbose_name='사용자 프로필'),
        ),
    ]
