import os
import sys
import time
import random
import asyncio
import aiohttp
import django
from async_iterator import AsyncIterator
from scraper import DataFetcher, DataDumper
from site_data import AGENTS, news_data
import secrs
sys.path.append(secrs.PROJECT_LOCATION)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_hub.settings')
django.setup()
from news.models import News

headers = {
	'User-Agent': random.choice(AGENTS),
}


async def get_response(session, url): # coroutine
	"""
	This function sends a request to the
	certain address and returns a response.
	"""
	async with session.get(url) as response:
		await asyncio.sleep(2)
		content = await response.text()
		return content


async def get_links(session, list_of_links=[]) -> list: # coroutine
	"""
	This function extracts the links of each news
	on the page.
	"""
	response = await get_response(session, news_data['gazeta_ru']['url'])
	links_parser = DataFetcher('gazeta_ru', news_data)
	links = links_parser.get_links(response)

	return links


async def get_tasks(session) -> list: # coroutine
	"""
	This function receives 
	a list of links.
	It then uses each of them in
	sending the requests and formatting
	a list of tasks.
	"""
	tasks = []
	links = await get_links(session)

	for i in range(0, len(links)):
		tasks.append(asyncio.create_task(get_response(session, links[i])))
	results = await asyncio.gather(*tasks)
	
	return results


async def extract_data(results, list_of_objs=[]) -> list: # coroutine
	"""
	This function receives a list
	of tasks as results of responses
	and does extract the data from each
	of them. It then returns a list of
	the objects formed from each result.
	"""
	content_parser = DataFetcher('gazeta_ru', news_data)
	
	for i in range(0, len(results)):
		obj = content_parser.fetch_data(results[i])
		list_of_objs.append(obj)

	return list_of_objs


async def create_record(obj):
	"""
	This function performs saving a
	single record to the database.
	"""
	model = News
	return model.objects.acreate(
			title=web_obj['title'],
			date=web_obj['date'],
			source=web_obj['source'],
			content=web_obj['content'],
			image=web_obj['image'],
			category=web_obj['category'],
		)


async def save_news(objects):
	"""
	This function receives a list of
	scraped objects, uses an asynchronous
	iterator to go through each item and make
	a record of each to the database.
	"""
	if len(objects) != 0:
			async for web_obj in AsyncIterator(objects):
				obj = await create_record(web_obj)
			else:
				print('The database has been updated.')
	else:
		print('No objects have been migrated to the DB.')


async def main() -> None: # coroutine
	"""
	This function initializes a session
	and gives a breathe to the other functions.
	Here are the results fetched and processed
	to the python dict objects, and the length
	of the list of such objects is shown.
	"""
	timeout = aiohttp.ClientTimeout(total=700)
	async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
		print(f'Start at {time.strftime("%X")}')
		results = await get_tasks(session)
		print(len(results))
		objects = await extract_data(results)
		print(len(objects))
		await save_news(objects)
		print(f'End at {time.strftime("%X")}')
		

asyncio.run(main())