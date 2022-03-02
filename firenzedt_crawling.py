import requests
from bs4 import BeautifulSoup
import pandas as pd

class Crawler:
    def __init__(self, firenzedt_url):
        self.firenzedt_url = firenzedt_url

    def get_url(self):
        url_list = {
            'politics': 'dummy data',
            'hanbando': 'dummy data',
            'international': 'dummy data',
            'policy': 'dummy data',
            'series': 'dummy data',
            'debate': 'dummy data',
            'weekend-culture': 'dummy data'
            }
        req = requests.get(self.firenzedt_url)
        soup = BeautifulSoup(req.text, 'html.parser')

        div = soup.select('nav > ul > li > a')
        div.pop()
        # When a category is added
        if len(url_list) < len(div):
            category = div[len(div)-1].get_text()
            # append the new category in the url_list
            url_list[category] = div[len(div)-1].get('href')
        # more than 2 categories are added
        # elif:
        # assign each hypertext reference to the corresponding category 
        else:
            url_list['politics'] = div[0].get('href')
            url_list['hanbando'] = div[1].get('href')
            url_list['international'] = div[2].get('href')
            url_list['policy'] = div[3].get('href')
            url_list['series'] = div[4].get('href')
            url_list['debate'] = div[5].get('href')
            url_list['weekend-culture'] = div[6].get('href')
            
        return url_list
    
    def get_metadata(self, url):
        
        return 0
        
def main():
    a = Crawler("https://firenzedt.com/") # argument should be an url which type is string
    url_list = a.get_url()
    for url in url_list.values():
        a.get_metadata(url)
    
    return 0

if __name__ == "__main__":
    main()