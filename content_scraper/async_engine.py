"""
This module manages HTTPS requests and 
responses in an asynchromous way, putting
the web scraping module into its work.
"""
import random
import asyncio
import aiohttp
from scraper import fetch_data, dump_data
import site_data


async def get_response(session, url):
	"""
	This function creates a single
	response per request.
	"""
	async with session.get(url) as response:
		return await response.text()


async def create_tasks(session, urls):
	"""
	This function wades through the
	list of links and processes all
	the	responses to the tasks.
	"""
	tasks = []

	for i in range(0, len(urls)):
		task = asyncio.create_task(get_response(urls[i]))
		tasks.append(task)

	results = await asyncio.gather(*tasks)
	return results


async def main():
	"""
	This function intializes the session.
	It then lets another function
	get the links of the objects
	and then all of the links are
	used to initialize requests to the
	tasks.
	"""
	async with aiohttp.ClientSession(headers={'User-Agent': random.choice(site_data.AGENTS)}) as session:
		results = await create_tasks(session)
		

asyncio.run(main())