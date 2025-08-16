from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ParticipantCount, UserProfile, MajorPopularity
from django.http import JsonResponse
import json

# 🟢 ذخیره رشته پیشنهادی
@csrf_exempt
def save_major(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            major_name = data.get('major')
            if major_name:
                obj, created = MajorPopularity.objects.get_or_create(major=major_name)
                obj.count += 1
                obj.save()
                return JsonResponse({'message': 'Saved successfully'})
            return JsonResponse({'error': 'major not found in request'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# 🟢 آمار صفحه لندینگ
@api_view(['GET'])
def landing_stats(request):
    count_obj = ParticipantCount.objects.first()
    total_participants = count_obj.total if count_obj else 0

    popular_major = (
        MajorPopularity.objects.values('major', 'count')
        .order_by('-count')
        .first()
    )

    return Response({
        'total_participants': total_participants,
        'most_popular_major': popular_major['major'] if popular_major else None
    })

# 🟢 توکن‌سازی JWT
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# 🟢 ثبت‌نام
@api_view(["POST"])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"message": "ایمیل و رمز عبور الزامی است"}, status=400)

    if User.objects.filter(username=email).exists():
        return Response({"message": "کاربری با این ایمیل وجود دارد"}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password)
    UserProfile.objects.create(email=email)

    count_obj, _ = ParticipantCount.objects.get_or_create(id=1)
    count_obj.total += 1
    count_obj.save()

    tokens = get_tokens_for_user(user)
    return Response({"token": tokens["access"]}, status=201)

# 🟢 ورود
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(username=email, password=password)
    if user is None:
        return Response({"message": "ایمیل یا رمز اشتباه است"}, status=401)

    tokens = get_tokens_for_user(user)

    count_obj, _ = ParticipantCount.objects.get_or_create(id=1)
    count_obj.total += 1
    count_obj.save()

    return Response({"token": tokens["access"]}, status=200)
