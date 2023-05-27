from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
	path('', views.HeadlineNewsView.as_view(), name='head_news'),
	path('<int:pk>/', views.NewsDetailsView.as_view(), name='news_details'),
]