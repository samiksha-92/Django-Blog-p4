from . import views
from django.urls import path
from .views import PostDetailView
from .views import CategoryPostsView
from .views import TagCreateView
from . views import PostLike
from .views import PostCreateView, PostUpdateView,PostDeleteView
from .views import CategoryCreateView, CategoryUpdateView,CategoryDeleteView,CategoryListView,TagListView,TagCreateView,TagDeleteView,TagUpdateView,TagDeleteView,TagPostsView
from .views import CommentListView



urlpatterns = [
path('', views.PostList.as_view(), name = 'home'),
path('post/new/', PostCreateView.as_view(), name='post_create'),
path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
path('category/new/', CategoryCreateView.as_view(), name='category_create'),
path('category/<slug:slug>/', CategoryPostsView.as_view(), name='category_posts'),
path('category/<slug:slug>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
path('category/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category_delete'),  
path('categories/', CategoryListView.as_view(), name='category_list'),
path('tag/create/', TagCreateView.as_view(), name='tag_create'),
path('tag/<slug:slug>/', TagPostsView.as_view(), name='tag_posts'),
path('tags/', TagListView.as_view(), name='tag_list'),  # List tags
path('tag/<int:pk>/edit/', TagUpdateView.as_view(), name='tag_edit'),  # Edit a tag
path('tag/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),  # Delete a tag
path('like/<slug:slug>/', PostLike.as_view(), name='post_like'),
path('search/',views.search_results, name='search_results'),
path('comments/', CommentListView.as_view(), name='comment_list'),
]



