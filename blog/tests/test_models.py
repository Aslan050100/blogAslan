from django.test import TestCase

from blog.models import Post


# Create your tests here.
class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Post.objects.create(author='eddy', )

    def setUp(self):
        # set up and refresh object used each time the test method is called.
        pass
