from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post,Comment,Category,Tag
from .forms import CommentForm
from django.utils import timezone

# Create your tests here.


class PostDetailViewTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a test category
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        # Create a test tag
        self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')

        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            category=self.category,
            text='This is a test post.',
            published_on=timezone.now(),
            status=1,
        )

        # Create a test comment
        self.comment = Comment.objects.create(
            post=self.post,
            name='Test Commenter',
            email='test@example.com',
            body='This is a test comment.',
            created_on=timezone.now(),
            approved=True,
        )

    def test_post_detail_view(self):
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.get(url)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct post is retrieved in the context
        self.assertEqual(response.context['post'], self.post)

        # Check if approved comments are retrieved and ordered correctly
        self.assertIn(self.comment, response.context['comments'])
        self.assertEqual(list(response.context['comments']), [self.comment])

        # Check if the comment form is present
        self.assertIn('comment_form', response.context)

        # Check if liked status is correctly set to False for anonymous user
        self.assertFalse(response.context['liked'])

        # Check if 'commented' flag is initially False
        self.assertFalse(response.context['commented'])

    def test_post_detail_view_post_method(self):
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.post(url, {'body': 'New test comment'})

        # Check if comment is successfully added
        self.assertTrue(Comment.objects.filter(body='New test comment').exists())

        # Check if 'commented' flag is set to True after adding comment
        self.assertTrue(response.context['commented'])







    
