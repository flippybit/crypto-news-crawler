from re import A
from typing import Text
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


# print("printing filterd links********************************************")
# for i ,link in enumerate (link_list):

#     if ("crypto" in str(link)):
#         print (i,link)

async def url_extractor(response_text):

    if (response_text is not None):

        for i ,link in enumerate (link_list):
            if ("crypto" in str(link)):
                print (i,link)
    return link


async def spider(session):
    async with session.get('http://www.coindesk.com/tag/bitcoin-mining') as resp:
             print( resp.status)
             return await resp.text()

async def main():
    async with aiohttp.ClientSession() as session:
        output = await asyncio.gather(spider(session))
        url = await url_extractor(output)
        print(url)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(spider())
asyncio.run(main())
