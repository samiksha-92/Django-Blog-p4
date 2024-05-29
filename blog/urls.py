from . import views
from django.urls import path
from .views import PostDetailView
from .views import CategoryPostsView
from .views import TagPostsView


urlpatterns = [
path('', views.PostList.as_view(), name = 'home'),
path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
path('category/<slug:slug>/', CategoryPostsView.as_view(), name='category_posts'),
path('tag/<slug:slug>/', TagPostsView.as_view(), name='tag_posts'),
]



