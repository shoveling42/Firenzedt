MAKE_JSON FUNCTION DOESN'T EXIST.

# Introduction

This repository contains crawling a table of Florence(피렌체의 식탁), a media website.

After executing `crawl.py`, you could collect the information on title, last edited date, author, url for each article.

# Prerequisites

    pip3 install requests
    pip3 install bs4

It could not matter what python version is, but it is recommended to use python 3.x (It might have been some issues using python 2.x)

# Cautions

Out of functions, update_article and store_main_txt could be implemented but not perfectly.

It means that you could utilize the former with some services which enable codes to be automatically executed like AWS Lambda, for instance.

Also, the latter could be executed incorrectly depending on article's structure.

# Restrictions

It is strongly required NOT to use the code commercially WITHOUT consent of Medici Media Co, Ltd((주)메디치미디어)!
