from django.urls import path, include
from . import views as blog_views
from blog.views import *

app_name = 'blog'

urlpatterns = [
	path('', PostList.as_view(), name='index'),
	path('about/', blog_views.about, name='about'),
	path('search/', Search.as_view(), name='search'),
	path('category/', CategoryList.as_view(), name='all-category'),
	path('category/<int:category>', PostCategoryList.as_view(), name='category'),
	path('article/<int:pk>/', PostView.as_view(), name='article'),
	path('article/<int:article_id>/comment/', blog_views.post_comment, name='comment'),
]

urlpatterns += [
	path('404/', error, name='error'),
]
