from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from .models import Post,Category,Tag,Comment
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .forms import CommentForm,PostForm,CategoryForm,TagForm
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

class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'
    success_url = reverse_lazy('post_detail')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name=self.request.user.username)

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    success_url = reverse_lazy('post_detail')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name=self.request.user.username)




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


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_form.html"
    success_url = reverse_lazy('home')


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_form.html"
    success_url = reverse_lazy('home')

class PostDeleteView(DeleteView):
    model = Post 
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy('home')



class CategoryPostsView(ListView):
    model = Post
    template_name = 'category_posts.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        return Post.objects.filter(category__slug=category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.category.name
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('home')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')



class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'  # Make sure the template is using this name

    def get_queryset(self):
        return Category.objects.all()  # Fetch all categories




class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tag_form.html'
    success_url = reverse_lazy('home')

class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tag_form.html'  
    success_url = reverse_lazy('tag_list')

class TagDeleteView(DeleteView):
    model = Tag
    template_name = 'tag_confirm_delete.html'  
    success_url = reverse_lazy('tag_list')


class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'  
    context_object_name = 'tags'


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


class CommentListView(ListView):
    model = Comment
    template_name = 'comment_list.html'  
    context_object_name = 'comments'    