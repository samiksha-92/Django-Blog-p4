from .models import Comment,Post,Category,Tag
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'category', 'tags', 'text', 'featured_image', 'status',]        