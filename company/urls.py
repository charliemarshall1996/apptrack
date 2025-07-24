from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    path("", views.CompanyListView.as_view(), name="list"),
    path("create/", views.CompanyCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.CompanyUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.CompanyDeleteView.as_view(), name="delete"),
]
