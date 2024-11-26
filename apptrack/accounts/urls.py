from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),
    path('profile-settings/<int:id>/',
         views.profile_settings_view, name='profile_settings'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html', success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('verify-email/<int:user_id>/<str:token>/',
         views.verify_email, name='verify_email'),
    path('resend-verification-email/', views.resend_verification_email,
         name='resend_verification_email'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
