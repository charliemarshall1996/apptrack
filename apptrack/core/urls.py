from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  path("", views.home_view, name="home"),
  path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
]