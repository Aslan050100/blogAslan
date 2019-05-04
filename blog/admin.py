from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'category', 'posted_time')
	list_filter = ['posted_time', 'category']
	search_fields = ['title', 'content']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
	list_display = ("article", 'name', 'posted_time', 'content', 'reply')
	list_filter = ['article']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", 'name')


admin.site.register(Tag)
