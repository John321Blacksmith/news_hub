"""
This module contains the main scraping tools
that are involved in an asynchronous work.
The functions below take a role in the web data
manipulation, whereas the async module manages
in performance speed.
"""
from bs4 import BeautifulSoup as Bs
# from news.models import News


class DataFetcher:
	"""
	This class creates an
	instanse capable of web data
	extraction.
	"""
	def __init__(self, item, site_dict):
		self.item = item
		self.site_dict = site_dict

	def get_soup(self, response=None, file_name=None, loc_file=False):
		"""
		This method creates a soup object.
		"""
		if loc_file:
			try:
				with open(file_name, mode='r', encoding='utf-8') as f:
					soup = Bs(f, 'html.parser')
			except FileNotFoundError:
				print('Couldn\'t find the file')
		else:
			soup = Bs(response, 'html.parser')

		return soup

	def get_links(self, response=None, file_name=None, loc_file=False, list_of_links = []) -> list:
		"""
		This method extracts the links
		of every object in the soup.
		"""
		if loc_file:
			soup = self.get_soup(file_name=file_name, loc_file=True)
		else:
			soup = self.get_soup(response)

		objs = soup.find_all(self.site_dict[self.item]['object']['tag'], self.site_dict[self.item]['object']['class'])
		
		for i in range(0, len(objs)):
			link = objs[i].find(self.site_dict[self.item]['obj_link']['tag'])
			list_of_links.append(self.site_dict[self.item]['url'][:21] + link['href'])

		return list_of_links



	def fetch_data(self, response=None, file_name=None, loc_file=False, obj={}) -> dict:
		"""
		This method receives a response object from every
		individual object page and extracts the
		necessary data.
		"""
		if loc_file:
			soup = self.get_soup(file_name=file_name, loc_file=True)
		else:
			soup = self.get_soup(response)

		if 'title' in self.site_dict[self.item]['obj_components']:
			title = soup.find(self.site_dict[self.item]['title']['tag'], self.site_dict[self.item]['title']['class'])
			if title:
				obj['title'] = title.text
			else:
				obj['title'] = 'no data'

		if 'date' in self.site_dict[self.item]['obj_components']:
			date = soup.find(self.site_dict[self.item]['date']['tag'], self.site_dict[self.item]['date']['class'])
			if date:
				try:
					obj['date'] = date['attribute']
				except KeyError:
					obj['date'] = '1999-07-02 06:00:00.000000-00:00'
			else:
				obj['date'] = '1999-07-02 06:00:00.000000-00:00'

		if 'source' in self.site_dict[self.item]['obj_components']:
			sources = soup.find_all(self.site_dict[self.item]['source']['tag'])
			for source in sources:
				for attr in source.attrs:
					if source[attr] == self.site_dict[self.item]['source']['keyword']:
						obj['source'] = source['href']
						break

		if 'content' in self.site_dict[self.item]['obj_components']:
			content = soup.find(self.site_dict[self.item]['content']['tag'], self.site_dict[self.item]['content']['class'])
			if content:
				obj['content'] = content.text
			else:
				obj['content'] = 'no data'

		if 'image' in self.site_dict[self.item]['obj_components']:
			image = soup.find(self.site_dict[self.item]['image']['tag'], self.site_dict[self.item]['image']['class'])
			if image:
				obj['image'] = image['src']
			else:
				obj['image'] = 'no data'

		if 'category' in self.site_dict[self.item]['obj_components']:
			category = soup.find(self.site_dict[self.item]['category']['tag'], self.site_dict[self.item]['category']['class'])
			if not category:
				obj['category'] = 'no data'
			else:
				obj['category'] = category

		return obj
