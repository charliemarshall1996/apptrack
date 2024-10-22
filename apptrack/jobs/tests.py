from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .views import JobsListView


class TestJobsListView(TestCase):
    def test_get_jobs_list_view(self):
        client = Client()
        response = client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)
