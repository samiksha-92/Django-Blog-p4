from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment
from django.utils import timezone

class ModelsTestCase(TestCase):

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
            excerpt='Test excerpt',
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

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Test Tag')
        self.assertEqual(self.tag.slug, 'test-tag')

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.text, 'This is a test post.')
        self.assertEqual(self.post.excerpt, 'Test excerpt')
        self.assertTrue(self.post.published_on)

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.name, 'Test Commenter')
        self.assertEqual(self.comment.email, 'test@example.com')
        self.assertEqual(self.comment.body, 'This is a test comment.')
        self.assertTrue(self.comment.created_on)
        self.assertTrue(self.comment.approved)

class ModelStringTestCase(TestCase):

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
            excerpt='Test excerpt',
            published_on='2024-01-01 12:00:00',
            status=1,
        )

        # Create a test comment
        self.comment = Comment.objects.create(
            post=self.post,
            name='Test Commenter',
            email='test@example.com',
            body='This is a test comment.',
            created_on='2024-01-02 12:00:00',
            approved=True,
        )

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_tag_str_method(self):
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_comment_str_method(self):
        expected_str = f"Comment This is a test comment. by Test Commenter"
        self.assertEqual(str(self.comment), expected_str)



class PostCommentsNumberTestCase(TestCase):

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
            published_on='2024-01-01 12:00:00',
            status=1,
        )

        # Create test comments
        self.comment1 = Comment.objects.create(
            post=self.post,
            name='Commenter 1',
            email='commenter1@example.com',
            body='Approved comment.',
            approved=True,
        )

        self.comment2 = Comment.objects.create(
            post=self.post,
            name='Commenter 2',
            email='commenter2@example.com',
            body='Not approved comment.',
            approved=False,
        )

        self.comment3 = Comment.objects.create(
            post=self.post,
            name='Commenter 3',
            email='commenter3@example.com',
            body='Another approved comment.',
            approved=True,
        )

    def test_number_of_comments_method(self):
        # Check the initial count of comments
        initial_count = self.post.comments.count()
        self.assertEqual(initial_count, 3)  # All comments

        # Check the count of approved comments using number_of_comments method
        approved_count = self.post.number_of_comments()
        self.assertEqual(approved_count, 2)  # Approved comments only
