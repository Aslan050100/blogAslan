from django.shortcuts import reverse
from django.test import TestCase

from blog.models import *


# Create your tests here.


class SearchViewTests(TestCase):

	@classmethod
	def setUpTestData(cls):
		# Create 14 posts with different keys in content for search tests with
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='key%s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num)
								)
		Post.objects.create(author=User.objects.create(username='eddy'),
							title='title14',
							content='key4',
							category=Category.objects.create(id=14, name='category14')
							)

	def test_created_database(self):
		# look at created database
		posts = Post.objects.all()
		for post in posts:
			pass  # print(['author:%s' % post.author, 'content:%s' % post.content])

	def test_page_accessed_by_url_name(self):
		response = self.client.get(reverse('blog:search') + '?key=4')
		self.assertEqual(response.status_code, 200)

	def test_page_exists_at_desired_location(self):
		response = self.client.get('/blog/search/?key=4')
		self.assertEqual(response.status_code, 200)

	def test_search_all_articles_with_same_key(self):
		response = self.client.get(reverse('blog:search') + '?key=4')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'eddy')
		self.assertContains(response, 'author 4')
		self.assertNotContains(response, 'author 3')

	def test_with_null_key(self):
		response = self.client.get(reverse('blog:search') + '?key=')
		categories = Category.objects.all()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'blog/search.html')
		self.assertContains(response, 'Do you search for:')
		self.assertContains(response, 'category14')
		self.assertNotContains(response, 'tag3')

	def test__with_valued_key(self):
		response = self.client.get(reverse('blog:search') + '?key=4')
		self.assertEqual(response.status_code, 200)

	def test_url_without_query(self):
		response = self.client.get(reverse('blog:search'))
		self.assertEqual(response.status_code, 200)


class PostListViewTests(TestCase):
	"""
	@classmethod
	def setUpTestData(cls):
		# Create 14 posts for pagination tests
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='content %s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num),
								)
	"""

	def test_empty_model(self):
		response = self.client.get(reverse('blog:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No posts yet!')

	def test_pagination_is_5(self):
		# Create 14 posts for pagination tests
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='content %s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num),
								)
		response = self.client.get(reverse('blog:index'))
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'] == True)
		self.assertTrue(len(response.context['post_list']) == 5)

	def test_page_accessed_by_url_name(self):
		# Create 14 posts for pagination tests
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='content %s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num),
								)
		response = self.client.get(reverse('blog:index'))
		self.assertEqual(response.status_code, 200)

	def test_page_exists_at_desired_location(self):
		# Create 14 posts for pagination tests
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='content %s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num),
								)
		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)

	def test_posts_ordered_by_reversed_id(self):
		# Create 14 posts for pagination tests
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='content %s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num),
								)
		response1 = self.client.get(reverse('blog:index') + '?page=3')
		self.assertEqual(response1.status_code, 200)
		[self.assertContains(response1, 'author %s' % num) for num in range(4)]
		self.assertNotContains(response1, 'author 4')

		response2 = self.client.get(reverse('blog:index') + '?page=1')
		self.assertEqual(response2.status_code, 200)
		[self.assertContains(response2, 'author %s' % num) for num in [9, 10, 11, 12, 13]]
		self.assertNotContains(response2, 'author 8')

	def test_page_uses_correct_template(self):
		# Create 14 posts for pagination tests
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='content %s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num),
								)
		response = self.client.get(reverse('blog:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Recent Post')
		self.assertTemplateUsed(response, 'blog/index.html')

	def test_list_all_posts(self):
		# Create 14 posts for pagination tests
		for post_num in range(14):
			Post.objects.create(author=User.objects.create(username='author %s' % post_num),
								title='title %s' % post_num,
								content='content %s' % post_num,
								category=Category.objects.create(id=post_num, name='category %s' % post_num),
								)
		# get the last page which is page 3, check display 4 items.
		response = self.client.get(reverse('blog:index') + '?page=3')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'] == True)
		self.assertTrue(len(response.context['post_list']) == 4)
