import requests
from bs4 import BeautifulSoup
import redis


class Scraper:
    def __init__(self, keywords):
        self.saved_links = []
        self.markup = requests.get('https://news.ycombinator.com/').text
        self.keywords = keywords

    def parse(self):
        soup = BeautifulSoup(self.markup, 'html.parser')
        links = soup.findAll("a", {"class": "storylink"})
        for link in links:
            for keyword in self.keywords:
                if keyword in link.text:
                    self.saved_links.append(link)

    def store(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        for link in self.saved_links:
            r.set(link.text, str(link))

    def email(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        [r.get(k) for k in r.keys()]
        print(r.keys())


Scraper(['developer'])
