import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, firenzedt_url):
        self.firenzedt_url = firenzedt_url
        
    def get_recent(self):
        refer_list = []
        refer = {
            'published': 'dummy data',
            'title': 'dummy data',
            'post_content': 'dummy data',
            'art_link': 'dummy data'
        }

        req = requests.get(self.firenzedt_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        published = soup.select('[class~="et_pb_ajax_pagination_container"] > article > p > span')
        title = soup.select('[class~="et_pb_ajax_pagination_container"] > article > h2')
        post_content = soup.select('[class~="et_pb_ajax_pagination_container"] > article > [class~="post-content"] > div > p')
        art_link = soup.select('[class~="et_pb_ajax_pagination_container"] > article > h2 > a')
        
        # 같은 기사가 2개씩 저장돼, 각각 list의 length를 반으로 줄임
        for idx in range(int(len(published)/2)):
            refer['published'] = published[idx].get_text()
            refer['title'] = title[idx].get_text()
            refer['post_content'] = post_content[idx].get_text()
            refer['art_link'] = art_link[idx].get('href')
            print(refer)
            refer_list.append(refer)

        return refer_list

    # def get_metadata(self):
    #     req = requests.get(self.firenzedt_url)
    #     soup = BeautifulSoup(req.text, 'html.parser')

    #     published = soup.select('[class~="et_pb_ajax_pagination_container"] > div > article > p > span')
    #     title = soup.select('[class~="column size-1of2"] > article > h2')
    #     post_content = soup.select('[class~="column size-1of2"] > article > [class~="post-content"] > div > p')
    #     art_link = soup.select('[class~="column size-1of2"] > article > h2 > a')
        
    #     print(published)
    #     print('\n')
    #     print(title)
    #     print('\n')
    #     print(post_content)
    #     print('\n')
    #     print(art_link)

    #     return 

def main():
    a = Crawler("https://firenzedt.com/") # argument should be an url which type is string
    print(a.get_recent())
    return 0

if __name__ == "__main__":
    main()