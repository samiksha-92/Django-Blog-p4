from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic, View
from .models import Post
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-published_on')
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
            # Check if user is authenticated before accessing email
            if request.user.is_authenticated:
                new_comment.email = request.user.email
                new_comment.name = request.user.username
            else:
                # Handle case for anonymous user (if needed)
                new_comment.email = 'anonymous@example.com'
                new_comment.name = 'Anonymous'

            new_comment.post = self.object
            new_comment.save()
            context['commented'] = True
        else:
            context['comment_form'] = comment_form  # Form with errors
            context['commented'] = False

        return self.render_to_response(context)
        # return render(request, self.template_name, context)


# @method_decorator(login_required, name='dispatch')
class PostLike(DetailView):
    model = Post
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = self.object
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))


class CategoryPostsView(ListView):
    model = Post
    template_name = 'category_posts.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=category_slug)


class TagPostsView(ListView):
    model = Post
    template_name = 'tag_posts.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        return Post.objects.filter(tags__slug=tag_slug)


def search_results(request):
    query = request.GET.get('query')
    if query:
        results = Post.objects.filter(title__icontains=query)
    else:
        results = []
    return render(request, 'search_results.html', {'results': results, 'query':query, })