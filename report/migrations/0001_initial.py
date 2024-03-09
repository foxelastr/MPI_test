# Generated by Django 5.0.2 on 2024-03-04 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ExamYearSemester', models.DateField(verbose_name='EXAM_YEAR_AND_SEMESTER')),
                ('ExamGrade', models.PositiveSmallIntegerField(verbose_name='EXAM_GRADE')),
                ('ExamArea', models.TextField(max_length=50, verbose_name='EXAM_AREA')),
                ('ExamResults', models.JSONField(default=list, verbose_name='EXAM_RESULTS')),
            ],
        ),
    ]
