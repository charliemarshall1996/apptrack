
import pytest

from blog.models import BlogPost


@pytest.mark.django_db
def test_blog_post(blog_post_data_factory):
    data = blog_post_data_factory()
    post = BlogPost(**data)
    assert post.title == data['title']
    assert post.content == data['content']
    assert post.summary == data['summary']
    assert post.published == data["published"]
    assert str(post) == data["title"]
