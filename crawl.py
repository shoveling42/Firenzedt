import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, firenzedt_url: str):
        self.firenzedt_url = firenzedt_url

    # get the last page of firenzedt website
    def get_last_page(self):
        max_page = 0
        req = requests.get(self.firenzedt_url)
        soup = BeautifulSoup(req.text, 'html.parser')

        # get the list of each page's link
        div = list(soup.select('[class~="nav-links"] > a'))
        div.pop(-1) # eliminate the duplicate tag

        # the number of last page
        for idx in range(len(div)):
            temp = int(div[idx].get_text())
            if (max_page < temp):
                max_page = temp

        return max_page

    # store all page's urls to utilize in the get_recent function
    def get_urls(self, last_page):
        url_list = []
        for idx in range(1, last_page+1):
            url = "https://firenzedt.com/page/{}?et_blog".format(idx)
            url_list.append(url)
        return url_list

    def get_author(self, meta_list):
        for idx in range(len(meta_list)):
            req = requests.get(meta_list[idx]['art_link'])
            soup = BeautifulSoup(req.text, 'html.parser')

            author = soup.select_one('[class~="author"]').get_text()
            
            meta_list[idx]['author'] = author

        return meta_list

    # get information on last_edited_date, title, content, urls about four lately articles.
    def get_recent(self):
        meta_recent = []

        req = requests.get(self.firenzedt_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        last_edited_date = soup.select('[class~="et_pb_ajax_pagination_container"] > article > p > span')
        title = soup.select('[class~="et_pb_ajax_pagination_container"] > article > h2')
        art_link = soup.select('[class~="et_pb_ajax_pagination_container"] > article > h2 > a')

        for idx in range(int(len(last_edited_date)/2)): # cut the same two articles in half
            refer = {
            'last_edited_date': 'dummy data',
            'title': 'dummy data',
            'art_link': 'dummy data'
        }
            refer['last_edited_date'] = last_edited_date[idx].get_text()
            refer['title'] = title[idx].get_text()
            refer['art_link'] = art_link[idx].get('href')

            meta_recent.append(refer)

        meta_recent = self.get_author(meta_recent)

        return meta_recent
    
    def update_article(self, meta_list, meta_recent):
        req = requests.get(self.firenzedt_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        new_article = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > h2 > a').get('href')
        
        # define two variables to distinguish whether an article is updated or not
        new = int(new_article[22:])
        latest = int(meta_recent[0]['art_link'][22:])
        
        # when an article is updated
        if (new > latest):
            refer = {
                'last_edited_date': 'dummy data',
                'title': 'dummy data',
                'art_link': 'dummy data'
            }
            last_edited_date = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > p > span')
            title = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > h2')
            art_link = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > h2 > a')
            # store last_edited_date, title, url in the new one
            refer['last_edited_date'] = last_edited_date.get_text()
            refer['title'] = title.get_text()
            refer['art_link'] = art_link.get('href')
            # descending sort of meta data by last_edited_date
            meta_list.insert(0, refer)

        return meta_list

    # get the meta data of the remaining except for the recent articles
    def get_remain(self, url_list):
        meta_remain = []
        
        # for each page
        for idx in range(len(url_list)):
            req = requests.get(url_list[idx])
            soup = BeautifulSoup(req.text, 'html.parser')

            last_edited_date = soup.select('[class~="et_pb_salvattore_content"] > article > p > span')
            title = soup.select('[class~="et_pb_salvattore_content"] > article > h2')
            art_link = soup.select('[class~="et_pb_salvattore_content"] > article > h2 > a')

            # store last_edited_date, title, url for each article
            for n in range(len(title)):
                refer = {
                'last_edited_date': 'dummy data',
                'title': 'dummy data',
                'art_link': 'dummy data'
            }

                refer['last_edited_date'] = last_edited_date[n].get_text()
                refer['title'] = title[n].get_text()
                refer['art_link'] = art_link[n].get('href')

                meta_remain.append(refer)
            
        meta_remain = self.get_author(meta_remain)

        return meta_remain
    
    # store paragraphs for each article
    def store_main_txt(self, meta_list):
        main_txt = []
        for idx in range(len(meta_list)):
            req = requests.get(meta_list[idx]['art_link'])
            soup = BeautifulSoup(req.text, 'html.parser')

            contents = soup.select('[class~="et_pb_post_content"] > p')
            
            main_txt.append(contents)
        return main_txt 

def main():
    a = Crawler("https://firenzedt.com/")
    last_page = a.get_last_page()
    url_list = a.get_urls(last_page)
    meta_recent = a.get_recent()
    meta_remain = a.get_remain(url_list)
    meta_list = meta_recent + meta_remain
    # meta_list = a.update_article(meta_list, meta_recent)
    # a.store_main_txt(meta_list)

if __name__ == "__main__":
    main()