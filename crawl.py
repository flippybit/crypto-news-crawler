from logging import Logger
import logging
from re import A
import re
import sys
from typing import Text
import aiofiles
from asyncio.queues import QueueEmpty
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import queue
from aiohttp import ClientSession

HREF_RE = re.compile(r'href="(.*?)"')

async def url_extractor(response):
    # Con set devuelvo una lista de links unicos sin repetir
    link_set = set()
    filterd_links = []
    soup = bs(response, "html.parser")
    print("The href links are :")
    for link in soup.find_all('a'):
    #    print(link.get('href'))
       link_set.add(link.get('href'))
    
    if (response is not None):
        
        for link in link_set:
           # se busca los link con la palabra "crypto"
           # y los links que no nos lleven fuera de la pagina (porque suele ser twitter)
            if ("crypto" in str(link) and "https:" not in str(link)):
                #  print (link)
                 filterd_links.append(link)

    print("end")
    return filterd_links


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    
    """Find HREFs in the HTML of `url`."""
    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logging.info(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logging.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found
    else:
        links = await url_extractor(html)
        logging.info("Found %d links for %s", len(found), url)
        return links

async def fetch_html(url: str, session: ClientSession) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """
    resp = await session.request(method="GET", url=url)
    resp.raise_for_status()
    # Logger.info("Got response [%s] for URL: %s", resp.status)
    html = await resp.text()
    return html
        

# async def write_one(file: IO, url: str, **kwargs) -> None:
#     """Write the found HREFs from `url` to `file`."""
#     res = await parse(url=url, **kwargs)
#     if not res:
#         return None
#     async with aiofiles.open(file, "a") as f:
#         for p in res:
#             await f.write(f"{url}\t{p}\n")
#         Logger.info("Wrote results for source URL: %s", url)

async def main():
    url ='http://www.coindesk.com/tag/bitcoin-mining'
   
    async with aiohttp.ClientSession() as ses:
        q = queue.Queue(50)
        q.put("http://www.coindesk.com/tag/bitcoin-mining")

        tasks = []
        output = await asyncio.gather(parse(session=ses, url=url))
        
        #url = await url_extractor(output)
        print("loop start ")
        for link in output[0]:
            q.put(link)

        print(f'size of queue:{q.qsize()}')
        
        while q.not_empty:
            try:
                next_url=q.get_nowait()
                print(next_url)
                tasks.append(parse(session=ses,url=url))
            except queue.Empty:
                print("empty queue JOB DONE!")
                break
                
            
print("fin")

# loop = asyncio.get_event_loop()
# loop.run_until_complete(spider())

if __name__ == "__main__":
    
   asyncio.run(main())
