from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.db.models import Q
from blog.models import Category, Comments, Post, Tag
from .forms import CommentForm
import markdown


# Create your views here.
class PostList(ListView):
	"""
	list view for index.html
	"""
	template_name = 'blog/index.html'
	# queryset = Post.objects.all()
	paginate_by = 5  # set numbers of posts per page.

	def get_queryset(self):
		results = Post.objects.all()
		for result in results:
			result.title = markdown.markdown(result.title, extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
			])
			result.content = markdown.markdown(result.content, extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
			])
		return results


class CategoryList(ListView):
	"""
	List all categories.
	"""
	model = Category
	template_name = 'blog/category_list.html'
	paginate_by = 10


class PostCategoryList(ListView):
	"""
	list all posts in a given category ordered by posted time.
	"""
	template_name = 'blog/category.html'
	paginate_by = 5

	def get_queryset(self):  # get queryset
		self.category = get_object_or_404(Category, id=self.kwargs['category'])
		return Post.objects.filter(category=self.category).order_by('-id')

	def get_context_data(self, **kwargs):  # pass extra arguments to template.
		context = super().get_context_data(**kwargs)
		context['category'] = self.category  # the variable name "category" will be used in template in {{category}}.
		return context


class Search(ListView):
	model = Post
	template_name = 'blog/search.html'
	paginate_by = 5

	def get_queryset(self):
		result = super(Search, self).get_queryset()
		queries = self.request.GET.get('key')
		if queries:
			result = Post.objects.filter(Q(title__icontains=queries) | Q(content__icontains=queries)).order_by('-id')
		return result

	def get_context_data(self, **kwargs):
		context = super(Search, self).get_context_data(**kwargs)
		context['tags'] = Tag.objects.all()
		context['categories'] = Category.objects.all()
		context['key'] = self.request.GET.get('key')
		return context


class PostView(DetailView):
	"""
	display an article's detail.
	"""
	model = Post
	template_name = 'blog/article.html'

	# inheritance Class DetailView and extend to define new attributes
	def __init__(self):
		self.comment_list = []  # the final list of comments
		self.top_level = []  # save top comments in a list
		self.sub_level = {}
		super().__init__()

	def get_object(self, queryset=None):
		queryset = Post.objects.get(id=self.kwargs['pk'])
		# markdown the content of the post
		queryset.content = markdown.markdown(queryset.content, extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.toc',
		])
		# also markdown the title if needed
		queryset.title = markdown.markdown(queryset.title, extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
		])
		return queryset

	# define comment function
	def comment_sort(self, comments):
		"""
		sort comments in a parent-kid recursive structure.
		:param comments: all comments belong to an article
		:return: sorted comment list of an article

		"""
		# use list generate expression to place instead of codes in block quotes above.
		[self.top_level.append(comment) for comment in comments if comment.reply is None]
		[self.sub_level.setdefault(comment.reply.id, []).append(comment) for comment in comments if
		 comment.reply is not None]
		[self.format_show(top_comment) for top_comment in self.top_level]  # call a recursive function
		for single_comment in self.comment_list:
			single_comment.content = markdown.markdown(single_comment.content, extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
			])
		return self.comment_list  # return sorted list of comments.

	def format_show(self, comment):
		"""
		:param comment: a parent comment
		:return: the list of parent comment and its kid comments
		"""
		self.comment_list.append(comment)
		try:
			kids = self.sub_level[comment.id]  # obtain all replay belongs to a comment.
		except KeyError:  # if no replay
			return self.comment_list  # end recursive
		else:
			[self.format_show(kid) for kid in kids]  # next recursive

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		# get session and save into context.
		try:
			context['session'] = {
				'name': self.request.session['name'],
				'email': self.request.session['email'],
				'content': self.request.session['content']
			}
		except Exception:  # do nothing if has exception
			pass

		# list comments
		comments = Comments.objects.filter(article=self.kwargs['pk'])  # query comments by post id.
		context['comment_list'] = self.comment_sort(comments)

		# pass comment form to template
		comment_form = CommentForm()
		context['comment_form'] = comment_form

		# get previous and next article id
		current_id = self.kwargs['pk']
		context['previous_id'] = current_id - 1

		if current_id == Post.objects.latest('id').id:
			context['next_id'] = None
		else:
			context['next_id'] = current_id + 1
		return context


def about(request):
	return render(request, 'blog/about.html')


def error(request):
	return render(request, 'blog/404.html')


@require_POST  # only accept a POST request; otherwise return a  django.http.HttpResponseNotAllowed
def post_comment(request, article_id):
	"""
	function to handle post request from comment form.
	if valid form, save form data into database and return a redirected page.
	if not, return previous page.
	:param article_id: captured from url.
	:param request: http POST request
	:return: redirected page if valid; otherwise, previous page with prompt message
	"""
	# session input to auto-fill
	request.session['name'] = request.POST.get('name')
	request.session['email'] = request.POST.get('email')
	comment = Comments()  # create a instance of Comments class
	comment.article = get_object_or_404(Post, pk=article_id)
	if request.POST.get('reply') != '0':  # if reply to a comment
		comment.reply = Comments.objects.get(pk=request.POST.get('reply'))  # get reply objective
	form = CommentForm(request.POST, instance=comment)
	# combine input form data and the instance to create a whole CommentForm instance
	if form.is_valid():  # if form is not valid
		try:
			messages.success(request, 'Your comment was added successfully!')
			form.save()  # save posted form date into database
			request.session['content'] = ''  # session nothing if successful
			return redirect('blog:article', article_id)
		except Exception:
			request.session['content'] = request.POST.get('content')  # save input content in session if fail
			messages.warning(request, 'AN EXCEPTION OCCURS!')
	messages.error(request, 'Please correct your error above!')  # if not a valid form
