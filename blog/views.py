from django.shortcuts import render
from django.views import generic
from .models import Post
from django.views.generic import DetailView
from django.views.generic import ListView
# Create your views here.

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status = 1).order_by('-published_on')
    template_name = 'index.html'
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class CategoryPostsView(ListView):
    model = Post
    template_name = 'category_posts.html'  #  template name
    context_object_name = 'post_list'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=category_slug)