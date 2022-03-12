import requests
from bs4 import BeautifulSoup
import re

class Crawler:
    def __init__(self, firenzedt_url):
        self.firenzedt_url = firenzedt_url

    # get the last page of firenzedt website
    def get_lastpage(self):
        max_page = 0
        req = requests.get(self.firenzedt_url)
        soup = BeautifulSoup(req.text, 'html.parser')

        # get the list of each page's link
        div = list(soup.select('[class~="nav-links"] > a'))
        div.pop(-1) # eliminate the duplicate tag which consists of next page-numbers class

        # count the number of last page
        for idx in range(len(div)):
            temp = int(div[idx].get_text())
            if (max_page < temp):
                max_page = temp

        return max_page

    # store all page's urls
    def get_allurl(self, last_page):
        url_list = []
        for idx in range(1, last_page+1):
            url = "https://firenzedt.com/page/{}?et_blog".format(idx)
            url_list.append(url)
        return url_list

    # get meta datum of recent 4 articles
    def get_recent(self):
        meta_list = []

        req = requests.get(self.firenzedt_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        published = soup.select('[class~="et_pb_ajax_pagination_container"] > article > p > span')
        title = soup.select('[class~="et_pb_ajax_pagination_container"] > article > h2')
        post_content = soup.select('[class~="et_pb_ajax_pagination_container"] > article > [class~="post-content"] > div > p')
        art_link = soup.select('[class~="et_pb_ajax_pagination_container"] > article > h2 > a')
        
        for idx in range(int(len(published)/2)): # cut the same two articles in half
            refer = {
            'published': 'dummy data',
            'title': 'dummy data',
            'post_content': 'dummy data',
            'art_link': 'dummy data'
        }
            # store published date, title, content, hyperlink in a article
            refer['published'] = published[idx].get_text()
            refer['title'] = title[idx].get_text()
            refer['post_content'] = post_content[idx].get_text()
            refer['art_link'] = art_link[idx].get('href')

            meta_list.append(refer)
        
        return meta_list
    
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
                'published': 'dummy data',
                'title': 'dummy data',
                'post_content': 'dummy data',
                'art_link': 'dummy data'
            }
            published = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > p > span')
            title = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > h2')
            post_content = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > [class~="post-content"] > div > p')
            art_link = soup.select_one('[class~="et_pb_ajax_pagination_container"] > article > h2 > a')
            # store published date, title, content, hyperlink in the new one
            refer['published'] = published.get_text()
            refer['title'] = title.get_text()
            refer['post_content'] = post_content.get_text()
            refer['art_link'] = art_link.get('href')
            # descending sort of meta datum by published date 
            meta_list.insert(0, refer)

        return meta_list

    # get the meta datum of the remaining except for the recent articles
    def get_remain(self, url_list):
        meta_list = []
        
        # for each page
        for idx in range(len(url_list)):
            req = requests.get(url_list[idx])
            soup = BeautifulSoup(req.text, 'html.parser')

            published = soup.select('[class~="et_pb_salvattore_content"] > article > p > span')
            title = soup.select('[class~="et_pb_salvattore_content"] > article > h2')
            post_content = soup.select('[class~="et_pb_salvattore_content"] > article > [class~="post-content"] > div > p')
            art_link = soup.select('[class~="et_pb_salvattore_content"] > article > h2 > a')

            # for each article, store published date, title, content, hyperlink
            for n in range(len(title)):
                refer = {
                'published': 'dummy data',
                'title': 'dummy data',
                'post_content': 'dummy data',
                'art_link': 'dummy data'
            }

                refer['published'] = published[n].get_text()
                refer['title'] = title[n].get_text()
                refer['post_content'] = post_content[n].get_text()
                refer['art_link'] = art_link[n].get('href')

                meta_list.append(refer)

        return meta_list

    # store main text for each article
    # contents 어디에 저장할 지는 작성되지 않음
    # 태그 제거하려면 주석 코드로 바꾸면 됨
    """
    def store_main_txt(self, meta_list):
        def CleanHtml(html):
            cleaner = re.compile('<.*?>')
            cleantext = re.sub(cleaner, '', html)
            return cleantext

        for idx in range(len(meta_list)):
            req = requests.get(meta_list[idx]['art_link'])
            soup = BeautifulSoup(req.text, 'html.parser')
            
            contents = CleanHtml(str(soup.select('[class~="et_pb_post_content"] > p')))
            
        return 0
    """
    def store_main_txt(self, meta_list):
        main_txt = []
        for idx in range(len(meta_list)):
            req = requests.get(meta_list[idx]['art_link'])
            soup = BeautifulSoup(req.text, 'html.parser')

            contents = soup.select('[class~="et_pb_post_content"] > p')
            
            main_txt.append(contents)
        return main_txt 

def main():
    a = Crawler("https://firenzedt.com/") # argument should be an url which type is string
    last_page = a.get_lastpage()
    url_list = a.get_allurl(last_page)
    meta_recent = a.get_recent()
    meta_remain = a.get_remain(url_list)
    meta_list = meta_recent + meta_remain
    # 기사 갱신 여부 어떻게 주기적으로 확인하나..
    meta_list = a.update_article(meta_list, meta_recent)
    a.store_main_txt(meta_list)

if __name__ == "__main__":
    main()