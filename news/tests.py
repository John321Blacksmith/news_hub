from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import News

# Create your tests here.


class NewsTest(TestCase):
	"""
	This test covers functionality
	of both news list & details pages.
	"""

	@classmethod
	def setUpTestData(cls):
		cls.timestamp0 = timezone.now()
		cls.news0 = News.objects.create(
					title='Test News',
					date=cls.timestamp0,
					source='https://test.dev',
					content='This is a main test block',
					image='https://static.test.com/img123.png',
					category='test',
				)
		cls.timestamp1 = timezone.now()
		cls.news1 = News.objects.create(
					title='Test News #2',
					date=cls.timestamp1,
					source='https://test.dev#2',
					content='This is a main test block#2',
					image='https://static.test.com/img123.png#2',
					category='test#2',
				)

	def test_model_data(self):
		self.assertEqual(self.news0.title, 'Test News')
		self.assertEqual(self.news0.date, self.timestamp0)
		self.assertEqual(self.news0.source, 'https://test.dev')
		self.assertEqual(self.news0.content, 'This is a main test block')
		self.assertEqual(self.news0.image, 'https://static.test.com/img123.png')
		self.assertEqual(self.news0.category, 'test')

	def test_url_exists_at_correct_loc_headline_news(self):
		response = self.client.get('/news/')
		self.assertEqual(response.status_code, 200)

	def test_url_available_via_name_headline_news(self):
		response = self.client.get(reverse('news:head_news'))
		self.assertEqual(response.status_code, 200)

	def test_url_exists_at_correct_loc_news_details(self):
		response = self.client.get('/news/1/')
		self.assertEqual(response.status_code, 200)

	def test_url_available_via_name_news_details(self):
		response = self.client.get(reverse('news:news_details', kwargs={'pk': self.news0.pk}))
		self.assertEqual(response.status_code, 200)

	def test_news_list_template(self):
		response = self.client.get(reverse('news:head_news'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'news/headline.html')
		self.assertContains(response, 'Test News')
		self.assertContains(response, 'Test News #2')

	def test_news_details_template(self):
		response = self.client.get(reverse('news:news_details', kwargs={'pk': self.news0.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'news/news_detail.html')

		self.assertContains(response, 'Test News')
		self.assertContains(response, 'https://test.dev')
		self.assertContains(response, 'This is a main test block')
		self.assertContains(response, 'https://static.test.com/img123.png')
		self.assertContains(response, 'test')
		
# passed