import requests
from bs4 import beautifulsoup4

resp = requests.get("http://www.google.com")
print(resp.text)