from django.urls import path
from accounts.views.api import ProfileAPI
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path('contact/', views.contact_view, name='contact'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('user-streak/<int:id>/', ProfileAPI.as_view(), name="user_streak")
]
