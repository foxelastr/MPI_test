# Generated by Django 5.0.2 on 2024-05-29 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='terms_agreed',
            field=models.BooleanField(default=False, verbose_name='전자상거래 표준약관 동의'),
        ),
    ]