from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Company
# Create your views here.


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'company/company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.filter(
            profile=self.request.user.profile
        )


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    fields = ["name", "is_recruiter", "website", "linkedin", "employees", "bio",
              "notes", "ignore"]
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('company:list')

    def form_valid(self, form):
        # Set the profile to the current user's profile before saving
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    fields = ["name", "is_recruiter", "website",
              "linkedin", "employees", "bio", "notes", "ignore"]
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('company:list')

    def get_queryset(self):
        # Restrict updates to the current user's companies
        return Company.objects.filter(profile=self.request.user.profile)


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = "company/company_confirm_delete.html"
    success_url = reverse_lazy('company:list')
