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
			link = objs[i].find(self.site_dict[self.item]['source']['tag'])
			list_of_links.append(self.site_dict[self.item]['url'][:21] + link['href'])

		return list_of_links

	def fetch_data(self, response=None, file_name=None, loc_file=False, obj={}) -> dict:
		"""
		This method gets a response from every
		individual object page and extracts the
		necessary data.
		"""
		if loc_file:
			soup = self.get_soup(file_name=file_name, loc_file=True)
		else:
			soup = self.get_soup(response)

		title = soup.find(self.site_dict[self.item]['title']['tag'], self.site_dict[self.item]['title']['class'])
		date = soup.find(self.site_dict[self.item]['date']['tag'], self.site_dict[self.item]['date']['class'])
		source = soup.find(self.site_dict[self.item]['source']['tag'])
		content = soup.find(self.site_dict[self.item]['content']['tag'], self.site_dict[self.item]['content']['class'])
		image = soup.find(self.site_dict[self.item]['image']['tag'], self.site_dict[self.item]['image']['class'])
		category = soup.find(self.site_dict[self.item]['category']['tag'], self.site_dict[self.item]['category']['class'])

		
		fields = ['title', 'date', 'source', 'content', 'image', 'category']
		values = [title, date, source, content, image, category]
		for i in range(0, len(values)):
			if values[i] is not None:
				if (fields[i] == 'date') or (fields[i] == 'source') or (fields[i] == 'image'):
					try:
						obj[fields[i]] = values[i]['attribute']
					except KeyError:
						obj[fields[i]] = values[i]
				else:
					obj[fields[i]] = values[i].text
			else:
				obj[fields[i]] = values[i]

		return obj


class News:
	pass


class DataDumper:
	"""
	This class creates an
	instance capable of dumping
	the scraped web data to the DB.
	"""
	def __init__(self, model):
		self.model = model

	def dump_data(self, objects: list):
		"""
		This receives a list of objects
		and saves each of the obects to the
		database via ORM system.
		"""
		if len(objects) != 0:
			for i in range(0, len(objects)):
				news = self.model.objects.create(
						title=objects[i]['title'],
						date=objects[i]['date'],
						source=objects[i]['source'],
						content=objects[i]['content'],
						category=objects[i]['category'],
					)

			else:
				print('The data has been saved to the DB')