import random
import asyncio
import aiohttp
from scraper import DataFetcher
from site_data import AGENTS, news_data


headers = {
	'User-Agent': random.choice(AGENTS),
}


async def get_response(session, url):
	async with session.get(url) as response:
		return await response.text()


async def get_tasks(session):
	tasks = []


async def exract_data(response):
	pass


async def main():
	async with aiohttp.ClientSession(headers=headers) as session:
		pass
	

asyncio.run(main())