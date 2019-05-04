from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


# Create your models here.
class Category(models.Model):
	id = models.IntegerField(primary_key=True, help_text='Enter a category id (e.g. 1)')
	name = models.CharField(max_length=100, unique=True, help_text='Enter a category (e.g. python)')

	class Meta:
		ordering = ['name']

	def get_absolute_url(self):
		"""Returns the url to access a particular instance of the model."""
		return reverse('blog:category', args=[str(self.id)])

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		pass


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	title = models.CharField(max_length=100, unique=True)
	content = models.TextField(help_text='Enter your post content here')
	posted_time = models.DateField('date posted', auto_now=True)
	category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
	tag = models.ManyToManyField(Tag)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		"""Returns the url to access a particular instance of the model."""
		return reverse('blog:article', args=[str(self.id)])


class Comments(models.Model):
	name = models.CharField(max_length=20)
	email = models.EmailField()
	content = models.TextField()
	posted_time = models.DateTimeField(auto_now=True)
	article = models.ForeignKey(Post, on_delete=models.CASCADE)
	reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		ordering = ['posted_time']

	def __str__(self):
		return self.content

	def get_absolute_url(self):
		"""Returns the url to access a particular instance of the model."""
		pass
