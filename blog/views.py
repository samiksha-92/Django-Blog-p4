from django.shortcuts import render
from django.views import generic
from .models import Post
from django.views.generic import DetailView
from django.views.generic import ListView
from .forms import CommentForm
# Create your views here.

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status = 1).order_by('-published_on')
    template_name = 'index.html'
    paginate_by = 5

from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Post
from .forms import CommentForm

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.filter(approved=True).order_by("-created_on")
        comment_form = CommentForm()
        liked = False
        if self.request.user.is_authenticated and post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['liked'] = liked
        context['commented'] = False
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Ensure 'self.object' is set
        context = self.get_context_data(**kwargs)
        
        # Process the submitted comment form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # If the form is valid, create a new comment
            new_comment = comment_form.save(commit=False)
            new_comment.email = request.user.email
            new_comment.name = request.user.username
            new_comment.post = self.object
            new_comment.save()
            context['commented'] = True  # Indicates that a comment has been submitted
        else:
            context['comment_form'] = comment_form  # Form with errors
            context['commented'] = False

        return render(request, self.template_name, context)



class CategoryPostsView(ListView):
    model = Post
    template_name = 'category_posts.html'  #  template name
    context_object_name = 'post_list'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=category_slug)


class TagPostsView(ListView):
    model = Post
    template_name = 'tag_posts.html'  #  template name
    context_object_name = 'post_list'

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        return Post.objects.filter(tags__slug=tag_slug)        