import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import get_openai_client
import os
from dotenv import load_dotenv
import re
from django.http import JsonResponse
from .models import SurveyResponse


load_dotenv()

def extract_json_from_response(text: str) -> str:
    """
    اگر متن با ```json شروع شده و با ``` تمام شده،
    آن بلاک کد را استخراج و فقط JSON داخلش را برمی‌گرداند.
    در غیر اینصورت متن بدون تغییر برمی‌گردد.
    """
    pattern = r"```json\s*(\{.*\})\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return text.strip()

@api_view(['POST'])
def submit_results(request):
    data = request.data
    print("✅ نتایج دریافت شد:", data)
    return Response({"message": "نتایج با موفقیت دریافت شد"})

@api_view(['POST'])
def chatgpt_analysis(request):
    answers = request.data.get("answers")
    print("📩 RAW request:", request.data)

    if not answers:
        return Response({"error": "❌ پاسخ‌ها دریافت نشدند"}, status=status.HTTP_400_BAD_REQUEST)

    prompt = f"""
شما یک مشاور حرفه‌ای هدایت شغلی هستید.
بر اساس پاسخ‌های زیر، یک تحلیل جامع ارائه دهید:

پاسخ‌های کاربر:
{json.dumps(answers, ensure_ascii=False, indent=2)}

پاسخ را در قالب JSON زیر بازگردان:
{{
  "detailed_analysis": "تحلیل جامع درباره مسیر شغلی کاربر...",
  "skill_roadmap": "مراحل مهارتی پیشنهادی...",
  "pros_and_cons": {{
    "pros": ["مزیت ۱", "مزیت ۲"],
    "cons": ["عیب ۱", "عیب ۲"]
  }},
  "learning_suggestions": "پیشنهاداتی برای یادگیری بعدی..."
}}
    """

    try:
        client = get_openai_client()
        print("🚀 ارسال درخواست به GPT از طریق آوالای...")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "شما یک دستیار مشاور شغلی هستید."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        print("✅ پاسخ از GPT دریافت شد")

        result_text = response.choices[0].message.content
        print("📨 خروجی خام GPT:\n", result_text)

        # پاک‌سازی بلاک کد Markdown اگر وجود داشت
        cleaned_text = extract_json_from_response(result_text)

        try:
            result_json = json.loads(cleaned_text)
            print("🟢 خروجی GPT با موفقیت به JSON تبدیل شد")
            return Response(result_json)

        except json.JSONDecodeError as decode_err:
            print("⚠️ خطا در تبدیل خروجی GPT به JSON:", decode_err)
            return Response({
                "error": "خروجی GPT فرمت JSON معتبری نداشت",
                "raw_output": result_text
            }, status=status.HTTP_502_BAD_GATEWAY)

    except Exception as e:
        error_message = str(e)
        print("❌ خطا در تماس با GPT:", error_message)

        if "401" in error_message or "invalid_api_key" in error_message:
            print("🔐 خطای 401 - کلید نامعتبر یا منقضی شده است")
            return Response({
                "error": "کلید API نامعتبر است. لطفاً کلید را بررسی کن."
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "error": "خطایی در پردازش GPT رخ داد",
            "details": error_message
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

print("🔑 استفاده از کلید:", os.getenv("OPENAI_API_KEY"))

@api_view(['GET'])
def landing_stats(request):
    all_results = SurveyResponse.objects.all() 
    total = all_results.count()

    majors = {}
    for result in all_results:
        first_answer = result.answers[0] if result.answers else None
        if first_answer:
            majors[first_answer] = majors.get(first_answer, 0) + 1

    most_popular = max(majors, key=majors.get) if majors else None

    return Response({
        'most_popular_major': most_popular,
        'total_participants': total,
    })
    return JsonResponse({'error': 'Method not allowed'}, status=405)
