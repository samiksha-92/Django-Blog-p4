from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Post, Comment, Category,Tag
from django.test import Client
class PostDetailViewTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')
        
        # Create a test category
        self.category = Category.objects.create(name='Test Category', slug='test-category')

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
        self.client.login(username='testuser', password='12345')  # Log in the test user
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.post(url, {
            'body': 'New test comment',
            'name': self.user.username,
            'email': self.user.email,
        })

        # Reload the post object to get the updated comments
        self.post.refresh_from_db()

        # Check if comment is successfully added
        self.assertTrue(Comment.objects.filter(body='New test comment').exists())

        # Check if 'commented' flag is set to True after adding comment
        response = self.client.get(url)
        self.assertTrue(response.context['commented'])


class CategoryPostsViewTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a test category
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        # Create test posts
        self.post1 = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            author=self.user,
            category=self.category,
            text='This is test post 1.',
            published_on=timezone.now(),
            status=1,
        )
        self.post2 = Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            author=self.user,
            category=self.category,
            text='This is test post 2.',
            published_on=timezone.now(),
            status=1,
        )

    def test_category_posts_view(self):
        url = reverse('category_posts', args=[self.category.slug])
        response = self.client.get(url)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'category_posts.html')

        # Check if the correct posts are retrieved in the context
        self.assertIn(self.post1, response.context['post_list'])
        self.assertIn(self.post2, response.context['post_list'])

        # Check if the number of posts retrieved is correct
        self.assertEqual(len(response.context['post_list']), 2)

class TagPostsViewTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a test tag
        self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')

        # Create test posts
        self.post1 = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            author=self.user,
            text='This is test post 1.',
            published_on=timezone.now(),
            status=1,
        )
        self.post2 = Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            author=self.user,
            text='This is test post 2.',
            published_on=timezone.now(),
            status=1,
        )

        # Assign the tag to the posts
        self.post1.tags.add(self.tag)
        self.post2.tags.add(self.tag)

    def test_tag_posts_view(self):
        url = reverse('tag_posts', args=[self.tag.slug])
        response = self.client.get(url)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'tag_posts.html')

        # Check if the correct posts are retrieved in the context
        self.assertIn(self.post1, response.context['post_list'])
        self.assertIn(self.post2, response.context['post_list'])

        # Check if the number of posts retrieved is correct
        self.assertEqual(len(response.context['post_list']), 2)


class SearchResultsViewTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            text='This is a test post.',
            status=1,
        )

    def test_search_results_view_with_results(self):
        url = reverse('search_results')
        query = 'Test'
        response = self.client.get(url, {'query': query})

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'search_results.html')

        # Check if 'query' is passed to the template context
        self.assertEqual(response.context['query'], query)

        # Check if 'results' in context contains the correct post
        self.assertIn(self.post, response.context['results'])

    def test_search_results_view_without_results(self):
        url = reverse('search_results')
        query = 'Nonexistent'
        response = self.client.get(url, {'query': query})

       
        self.assertEqual(response.status_code, 200)

        
        self.assertTemplateUsed(response, 'search_results.html')

        
        self.assertEqual(response.context['query'], query)

        
        self.assertEqual(list(response.context['results']), [])
    


class PostLikeViewTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a test category
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            category=self.category,
            text='This is a test post.',
            excerpt='Test excerpt',
            status=1,
        )

        # Create a client and login
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_post_like_view_like(self):
        # Send a POST request to like the post
        response = self.client.post(reverse('post_like', args=[self.post.slug]))
        
        # Refresh the post instance from the database
        self.post.refresh_from_db()

        # Check if the user is in the list of likes
        self.assertIn(self.user, self.post.likes.all())

        # Check if the response is a redirect to the post detail view
        self.assertRedirects(response, reverse('post_detail', args=[self.post.slug]))

    def test_post_like_view_unlike(self):
        # First, like the post
        self.post.likes.add(self.user)

        # Send a POST request to unlike the post
        response = self.client.post(reverse('post_like', args=[self.post.slug]))

        # Refresh the post instance from the database
        self.post.refresh_from_db()

        # Check if the user is not in the list of likes
        self.assertNotIn(self.user, self.post.likes.all())

        # Check if the response is a redirect to the post detail view
        self.assertRedirects(response, reverse('post_detail', args=[self.post.slug]))
