import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

# 사용자 조회 및 사용자 프로필 생성 로직
user = User.objects.get(username='your_username')
UserProfile.objects.create(user=user)

print("UserProfile created for:", user.username)
