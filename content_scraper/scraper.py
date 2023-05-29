"""
This module contains the main scraping tools
that are involved in an asynchronous work.
The functions below take a role in the web data
manipulation, whereas the async module manages
in performance speed.

This class creates an
instanse capable for web data
extraction.

This class creates an
instance capable for dumping
the scraped web data to the DB.
"""
from bs4 import BeautifulSoup as Bs
from news.models import News


def fetch_data(resp, item, site_dict: dict, list_of_objs=[]):

	soup = Bs(resp, 'html.parser')

	objects = soup.select(site_dict[item]['object'])

	for i in range(0, len(objects)):
		obj = {
			'title': objects[i].select_one(site_dict['title']),
			'date': objects[i].select_one(site_dict['date']),
			'source': objects[i].select_one(site_dict['source']),
			'content': objects[i].select_one(site_dict['content']),
			'image': objects[i].select_one(site_dict['image']),
			'category': objects[i].select_one(site_dict['category']),
		}
		list_of_objs.append(obj)

	return list_of_objs


def dump_data(objects: list):
	model = News
	if len(objects) != 0:
		for i in range(0, len(objects)):
			news = model.objects.create(
					title=objects[i]['title'],
					date=objects[i]['date'],
					source=objects[i]['source'],
					content=objects[i]['content'],
					category=objects[i]['category'],
				)

		else:
			print('The data has been saved to the DB')