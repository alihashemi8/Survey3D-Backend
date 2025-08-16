from django.urls import path
from . import views

urlpatterns = [
    path("api/register/", views.register, name="register"),
    path("api/login/", views.login, name="login"),
    path("api/landing-stats/", views.landing_stats, name="landing-stats"),
    path("save-major/", views.save_major, name="save-major"),
]
