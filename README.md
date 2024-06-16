# Yogit Blog: Balancing Bytes with Breath

Welcome to **Yogit Blog**, where we harmoniously blend the worlds of coding and yoga. Our mission is to provide developers with insightful tips on integrating yoga practices into their daily routines, promoting a balanced lifestyle that enhances both mental agility and physical wellness.

## Overview

**Yogit Blog** is a unique platform dedicated to helping developers achieve a healthy work-life balance. Our content is tailored to offer practical advice on maintaining mental clarity and physical health while navigating the demanding field of software development. Whether you're a seasoned coder or a beginner, our blog posts aim to enrich your life with the benefits of yoga, making every byte you code a breath of fresh air.

## Key Features

- **Insightful Blog Posts**: Our articles cover a wide range of topics, from coding best practices to yoga techniques that help alleviate stress and improve focus. Coding best practices posts will follow soon.
- **Search Functionality**: Easily find posts that interest you with our intuitive search feature.
- **Responsive Design**: Our website is designed to be fully responsive, ensuring a seamless experience across all devices. Post images will not appear on smaller screens
- **Engaging Content**: Each post includes an excerpt and a featured image, providing a quick overview and visual appeal.
- **Categories/Tagst**: Each post belongs to a specific category and multiple tags. Making it easy for readers to search a relevant topic.

## Technology Stack

- **Frontend**: HTML, CSS, Bootstrap for a responsive and visually appealing design.
- **Backend**: Django framework, ensuring a robust and scalable structure.
- **Database**: postgresql, providing efficient data management.
- **Hosting**: The blog is hosted on Heroku - reliable cloud platform, ensuring high availability and performance for a smaller application, like this blog.

## Getting Started

To get started with Yogit Blog, follow these simple steps:

1. **Clone the repository**: `git clone https://github.com/yourusername/yogit-blog.git`
2. **Navigate to the project directory**: `cd yogit-blog`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run migrations**: `python manage.py migrate`
5. **Start the development server**: `python manage.py runserver`
6. **Visit the blog**: Open your browser and go to `http://127.0.0.1:8000`

## Test Cases Overview - Automated & Manual

### Post Comment View Test Cases

**Conclusion:** This test case verifies the functionality related to commenting on a post.

**Explanation:** 
- **test_post_detail_view:** Checks if the post detail view renders correctly and if approved comments are displayed in the context. It also verifies that the comment form and other context variables are present and correctly initialized.
  
- **test_post_detail_view_post_method:** Tests the behavior when a user posts a new comment. It ensures that the comment is successfully added to the database and that the 'commented' flag in the context is set to True after the comment is posted and approved.

### Category Posts View Test Case

**Conclusion:** This test case validates the category-specific post listing functionality.

**Explanation:**
- **test_category_posts_view:** Ensures that the category posts view renders the correct template and retrieves the appropriate posts associated with a specific category. It checks if the posts are present in the context and verifies the count of retrieved posts.

### Tag Posts View Test Case

**Conclusion:** This test case verifies the tag-specific post listing functionality.

**Explanation:**
- **test_tag_posts_view:** Checks if the tag posts view renders the correct template and retrieves the correct posts associated with a specific tag. It verifies that the retrieved posts are present in the context and confirms the count of retrieved posts.

### Search Results View Test Case

**Conclusion:** This test case validates the search functionality and its results.

**Explanation:**
- **test_search_results_view_with_results:** Tests the search results view when there are matching results for a query. It verifies that the correct template is rendered, the search query is passed to the context, and the expected post is present in the results.

- **test_search_results_view_without_results:** Validates the search results view when there are no matching results for a query. It checks that the correct template is rendered, the search query is passed to the context, and the results list is empty.

### Post Like View Test Case

**Conclusion:** This test case verifies the functionality related to liking and unliking posts.

**Explanation:**
- **test_post_like_view_like:** Tests the functionality of liking a post. It sends a POST request to like a post and verifies that the user is added to the list of likes for that post. It also checks that the response redirects back to the post detail view after liking.

- **test_post_like_view_unlike:** Validates the functionality of unliking a post. It first likes the post by adding the user to the list of likes, then sends a POST request to unlike the post and verifies that the user is removed from the list of likes. It confirms that the response redirects back to the post detail view after unliking.

These test cases cover essential functionalities of the Yogit Blog application, ensuring that features like post detail viewing, category and tag filtering, search functionality, and post liking operate correctly and reliably under different scenarios. Running these tests helps maintain the application's integrity and functionality across updates and modifications.
