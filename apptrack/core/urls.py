from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  path("", views.home_view, name="home"),
  path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
  path('contact/', views.ContactView.as_view(template_name='core/contact.html'), name='contact'),
  path('get-subdivisions/<str:country_code>/', views.get_subdivisions, name='get_subdivisions'),
  path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
]