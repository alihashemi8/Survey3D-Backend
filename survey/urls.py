from django.urls import path
from .views import chatgpt_analysis, submit_results , landing_stats
from . import views


urlpatterns = [
    path('chatgpt_analysis/', chatgpt_analysis),
    path('submit/', submit_results),
    path('landing-stats/', landing_stats),


]
