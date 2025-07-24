from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("contact/", views.contact_view, name="contact"),
    path("privacy-policy/", views.privacy_policy_view, name="privacy_policy")
]
