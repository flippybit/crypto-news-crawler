import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs

resp = requests.get("http://www.coindesk.com/tag/bitcoin-mining")

soup = bs(resp.text)
print(soup.prettify())
link_list = []
soup = bs(resp.text, "html.parser")
print("The href links are :")
for link in soup.find_all('a'):
   print(link.get('href'))
   link_list.append(link.get('href'))


print("printing filterd links********************************************")
for i ,link in enumerate (link_list):

    if ("crypto" in str(link)):
        print (i,link)


async def spider():
    async with aiohttp.ClientSession() as session:
         async with session.get('http://httpbin.org/get') as resp:
                print(resp.status)
                print(await resp.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(spider())
