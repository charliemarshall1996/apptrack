"""Houses the JobListView class.

Manages the job list view.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from jobs.models import Job
from jobs.forms import JobForm, JobFilterForm


class JobListView(LoginRequiredMixin, ListView):
    """Manages the job list view.

    Inherits from the ListView class and adds a form to the context.
    It provides functionality to paginate and filter the job list for the requesting 
    user.

    Attributes:
        model (class): The model class for the view.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the object in the context.
        paginate_by (int): The number of items to display per page.
        ordering (str): The field to order the queryset by.
    """

    model = Job
    template_name = "jobs/list.html"
    context_object_name = "jobs"
    paginate_by = 10
    ordering = ["-updated"]

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

    def get_queryset(self):
        """Get the filtered queryset.

        Gets the queryset from the parent class and filters it.
        It always filters by the user's profile. After that, it uses fields and values
        from the JobFilterForm to filter the queryset.

        Returns:
            QuerySet: The filtered queryset.
        """
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
                queryset = queryset.filter(company__icontains=company)

            # Check if the city filter is set
            if city:
                queryset = queryset.filter(city__icontains=city)

            # Check if the region filter is set
            if region:
                queryset = queryset.filter(region__icontains=region)

            # Check if the countries filter is set
            if countries:
                queryset = queryset.filter(country__in=countries)

        # Return the filtered queryset
        return queryset

    def get_context_data(self, **kwargs):
        """Get the context data for the job list view.

        Adds the user ID, filter form, and a blank job form to the
        context.

        Returns:
            dict: The context data.
        """
        jobs = Job.objects.filter(
            profile=self.request.user.profile, archived=False).all()
        edit_forms = {job.id: JobForm(instance=job) for job in jobs}
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["filter_form"] = JobFilterForm(
            self.request.GET
        )  # Pass form to template

        context["edit_forms"] = edit_forms

        context["job_form"] = JobForm()
        return context
