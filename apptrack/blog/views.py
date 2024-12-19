from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
# Create your views here.

from .models import BlogPost


def home(request):
    posts_list = BlogPost.objects.only("id", "title", "summary", "published")
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page

    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "blog/home.html", {"posts": posts})


def post(request, id):
    post = get_object_or_404(BlogPost, id=id)

    return render(request, "blog/post.html", {"post": post})
