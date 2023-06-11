from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from .forms import CommentForm
from .models import News, Comment

# Create your views here.


class HeadlineNewsView(ListView):
	"""
	This view represents a bunch of
	most important news that are
	located on the main page.
	"""
	model = News
	template_name = 'news/headline.html'


class CommentGet(DetailView):
	"""
	This view handles just receiving
	the body via GET http method.
	"""
	model = News
	tmplate_name = 'news/news_details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm()
		return context


class CommentPost(SingleObjectMixin, FormView):
	"""
	This view handles sending
	the data the user provides in the
	entry body via POST http method.
	"""
	model = News
	form_class = CommentForm
	template_name = 'news/news_details.html'

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.news = self.object
		comment.save()

		return super().form_valid(form)

	def get_success_url(self):
		news = self.get_object()
		return reverse('news:news_details', kwargs={'pk': news.pk})


class NewsDetailsView(LoginRequiredMixin, DetailView, View):
	"""
	This view does render the detail page
	involving both POST and GET handler views.
	"""

	def get(self, request, *args, **kwargs):
		"""
		This method activates the GET view.
		"""
		view = CommentGet.as_view()
		return view(request, *args, **kwargs)
		

	def post(self, request, *args, **kwargs):
		"""
		This method activates the POST view.
		"""
		view = CommentPost.as_view()
		return view(request, *args, **kwargs)
		