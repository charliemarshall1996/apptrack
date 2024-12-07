from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_blog_home_view(client):
    url = reverse('blog:home')
    response = client.get(url)
    assert response.status_code == 200
