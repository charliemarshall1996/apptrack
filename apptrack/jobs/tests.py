from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Jobs
from .views import JobsListView

User = get_user_model()


class TestJobsListView(TestCase):

    def test_view_requires_login(self):
        client = Client()
        response = client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 302)

    def test_get_logged_in_view(self):
        user = User.objects.create_user(
            email='testuser@test.com', password='password')
        self.client.login(email='testuser@test.com', password='password')
        url = reverse('jobs:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_gets_users_jobs(self):
        user = User.objects.create_user(
            email='testuser@test.com', password='password')
        Jobs.objects.create(user=user)
        jobs = Jobs.objects.filter(user=user)
        self.client.login(email='testuser@test.com', password='password')
        url = reverse('jobs:list')
        response = self.client.get(url)
        queryset = response.context['object_list']
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(queryset, jobs)
