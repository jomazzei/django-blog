from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    # Filters to only display published blogs on home page, not drafts
    queryset = Post.objects.all().order_by("-created_on").filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6