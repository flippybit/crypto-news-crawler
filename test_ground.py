from logging import Logger
import logging
from re import A
import sys
from typing import Text
import aiofiles
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import queue
from aiohttp import ClientSession

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
