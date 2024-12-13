
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from jobs.models import Job
from jobs.forms import JobForm, JobFilterForm


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    ordering = ['-updated']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile=self.request.user.profile)
        form = JobFilterForm(self.request.GET)

        if form.is_valid():
            statuses = form.cleaned_data.get('status')
            title = form.cleaned_data.get('title')
            job_functions = form.cleaned_data.get('job_functions')
            company = form.cleaned_data.get('company')
            city = form.cleaned_data.get('city')
            region = form.cleaned_data.get('region')
            countries = form.cleaned_data.get('countries')
            archived = form.cleaned_data.get('archived')
            if archived != 'in':
                if archived == 'on':
                    queryset = queryset.filter(archived=True)
                else:
                    queryset = queryset.exclude(archived=True)

            if statuses:
                queryset = queryset.filter(status__in=statuses)
            if title:
                queryset = queryset.filter(job_title__icontains=title)
            if job_functions:
                queryset = queryset.filter(job_function__in=job_functions)
            if company:
                queryset = queryset.filter(company__icontains=company)
            if city:
                queryset = queryset.filter(city__icontains=city)
            if region:
                queryset = queryset.filter(region__icontains=region)
            if countries:
                queryset = queryset.filter(country__in=countries)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        context['filter_form'] = JobFilterForm(
            self.request.GET)  # Pass form to template
        context['job_form'] = JobForm()
        return context
