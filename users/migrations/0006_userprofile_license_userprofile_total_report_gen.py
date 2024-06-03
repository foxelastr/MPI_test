# Generated by Django 5.0.2 on 2024-05-29 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userprofile_terms_agreed'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='license',
            field=models.PositiveIntegerField(default=5, verbose_name='사용권(남은 횟수)'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_report_gen',
            field=models.PositiveIntegerField(default=0, verbose_name='보고서 생성 횟수'),
        ),
    ]
