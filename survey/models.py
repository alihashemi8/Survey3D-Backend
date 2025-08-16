from django.db import models

class SurveyResponse(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField()

    def __str__(self):
        return f"Response at {self.timestamp}"
