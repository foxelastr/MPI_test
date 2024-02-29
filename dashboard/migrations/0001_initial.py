# Generated by Django 5.0.2 on 2024-02-25 03:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, unique=True)),
                ('birthdate', models.DateField(verbose_name='BIRTHDATE')),
                ('grade', models.PositiveSmallIntegerField(verbose_name='GRADE')),
                ('Consulting_schedule', models.DateTimeField(blank=True, null=True, verbose_name='SCHEDULE')),
                ('Consulting_content', models.TextField(blank=True, help_text='상담 내용을 적으세요.', max_length=200, verbose_name='CONTENT')),
                ('Consulting_status', models.BooleanField(default=False, verbose_name='CONSULTING STATUS')),
                ('Test_date', models.DateField(auto_now_add=True, verbose_name='Test_date')),
                ('Test_list', models.ManyToManyField(to='dashboard.test_list')),
            ],
        ),
        migrations.CreateModel(
            name='Test_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='CREATE DT')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.student')),
            ],
        ),
    ]
