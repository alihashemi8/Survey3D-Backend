from rest_framework import serializers
from .models import SurveyResponse

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'
