from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_blog_home_view(client):
    url = reverse('blog:home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_blog_post_view(client, blog_post_factory):
    post = blog_post_factory()
    post.save()
    url = reverse("blog:post", args=[post.pk])
    response = client.get(url)
    assert response.status_code == 200
