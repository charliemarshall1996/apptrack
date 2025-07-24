"""Houses the JobListView class.

Manages the job list view.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from company.models import Company
from jobs.models import Job
from jobs.forms import JobForm, JobFilterForm


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "jobs/list.html"
    context_object_name = "jobs"
    paginate_by = 10
    ordering = ["-updated"]

    def get_ordering(self):
        """Get the ordering for the queryset based on the request parameters."""
        ordering = self.request.GET.get('ordering', '-updated')
        return ordering

    def get_queryset(self):
        """Get the filtered and sorted queryset."""
        queryset = super().get_queryset()
        queryset = queryset.filter(profile=self.request.user.profile)

        # Get the form
        form = JobFilterForm(self.request.GET)

        # If the form is valid, filter the queryset
        if form.is_valid():
            statuses = form.cleaned_data.get("status")
            title = form.cleaned_data.get("title")
            job_functions = form.cleaned_data.get("job_functions")
            company = form.cleaned_data.get("company")
            city = form.cleaned_data.get("city")
            region = form.cleaned_data.get("region")
            countries = form.cleaned_data.get("countries")
            archived = form.cleaned_data.get("archived")
            queryset = self._archive_filter(queryset, archived)

            # Check if the statuses filter is set
            if statuses:
                queryset = queryset.filter(status__in=statuses)

            # Check if the title filter is set
            if title:
                queryset = queryset.filter(job_title__icontains=title)

            # Check if the job functions filter is set
            if job_functions:
                queryset = queryset.filter(job_function__in=job_functions)

            # Check if the company filter is set
            if company:
                companies = Company.objects.filter(
                    name__icontains=company, profile=self.request.user.profile)
                companies = [company.id for company in companies]
                queryset = queryset.filter(company__in=companies)

            # Check if the city filter is set
            if city:
                queryset = queryset.filter(city__icontains=city)

            # Check if the region filter is set
            if region:
                queryset = queryset.filter(region__icontains=region)

            # Check if the countries filter is set
            if countries:
                queryset = queryset.filter(country__in=countries)

        # Order the queryset
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        """Get the context data for the job list view."""
        jobs = Job.objects.filter(
            profile=self.request.user.profile, archived=False).all()
        edit_forms = {job.id: JobForm(instance=job) for job in jobs}
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["filter_form"] = JobFilterForm(self.request.GET)
        context["edit_forms"] = edit_forms
        context["job_form"] = JobForm()
        context["ordering"] = self.get_ordering()
        return context

    def _archive_filter(self, queryset, filter_val):
        """Archive filter helper.

        Takes a queryset and a filter value and filters the queryset according to the
        filter value.

        Args:
            queryset (QuerySet): The queryset to filter.
            filter_val (str): The filter value. Must be one of "in", "on", or "ex".

        Returns:
            QuerySet: The filtered queryset.
        """
        if filter_val != "in":
            # If the archived filter is set to "only",
            # filter the queryset to show only archived jobs
            if filter_val == "on":
                queryset = queryset.filter(archived=True)

            # If the archived filter is set to "exclude",
            # filter the queryset to exclude archived jobs
            else:
                queryset = queryset.exclude(archived=True)

        return queryset
