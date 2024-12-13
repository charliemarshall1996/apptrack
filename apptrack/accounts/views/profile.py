import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'  # Adjust based on your template
    slug_field = 'id'  # Or 'slug' if you use a custom slug field
    slug_url_kwarg = 'slug'  # This is the URL parameter expected

    # Override get_object to use the logged-in user
    def get_object(self):
        # Return the logged-in user based on the slug
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context
