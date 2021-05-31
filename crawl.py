import requests
from bs4 import beautifulsoup4

resp = requests.get("www.coindesk.com")
print(resp.text)