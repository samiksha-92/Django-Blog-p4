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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if self.request.user.is_authenticated and post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['comments'] = comments
        context['liked'] = liked
        return context


class CategoryPostsView(ListView):
    model = Post
    template_name = 'category_posts.html'  #  template name
    context_object_name = 'post_list'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=category_slug)


class TagPostsView(ListView):
    model = Post
    template_name = 'tag_posts.html'  # Your template name
    context_object_name = 'post_list'

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        return Post.objects.filter(tags__slug=tag_slug)        