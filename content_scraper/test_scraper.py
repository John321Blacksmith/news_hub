import random
import asyncio
import aiohttp
from scraper import DataFetcher
from site_data import AGENTS, news_data


headers = {
	'User-Agent': random.choice(AGENTS),
}


async def get_response(session, url): # coroutine
	async with session.get(url) as response:
		return await response.text()


async def get_links(list_of_links=[]): # coroutine
	"""
	This function extracts the links of each news
	on the page.
	"""
	links_parser = DataFetcher('gazeta_ru', news_data)
	links = links_parser.get_links(file_name='ht.html', loc_file=True)

	return links


async def get_tasks(session): # coroutine
	"""
	This function receives 
	a list of links to be
	used in sending the requests.
	"""
	tasks = []
	links = await get_links()

	for i in range(0, len(links)):
		tasks.append(asyncio.create_task(get_response(session, links[i])))

	results = await asyncio.gather(*tasks)

	return results


async def extract_data(results, list_of_objs=[]): # coroutine
	content_parser = DataFetcher('gazeta_ru', news_data)
	
	for i in range(0, len(results)):
		obj = content_parser.fetch_data(results[i])
		list_of_objs.append(obj)


async def main(): # coroutine
	async with aiohttp.ClientSession(headers=headers) as session:
		results = await get_tasks(session)
		objects = await extract_data(results)
		print(len(objects))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())