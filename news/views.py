from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import News

# Create your views here.


class HeadlineNewsView(ListView):
	"""
	This view represents a bunch of
	most important news that are
	located on the main page.
	"""
	model = News
	template_name = 'news/headline.html'


class NewsDetailsView(DetailView):
	"""
	This view shows a detail page of
	a single news.
	"""
	model = News
	template_name = 'news/news_detail.html'