from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post,Comment,Category,Tag
from .forms import CommentForm

# Create your tests here.

class PostListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 10 published posts 
        number_of_posts = 10
        for post_id in range(number_of_posts):
            Post.objects.create(
                title = f'Test post {post_id}',
                text = 'This is a test post',
                status = '1',
                published_on='2023-06-01'

            )
    def setUp(self):
        self.client = Client()

    def test_view_url_exists_correctly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_desired_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response,'index.html')

    def test_view_is_paginated(self):
        response = self.client.get(reverse('home'))
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['post_list']),5)





    
