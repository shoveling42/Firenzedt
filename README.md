# Introduction

This repository contains crawling a table of Florence(피렌체의 식탁), a media website. After executing `crawl.py`, you could collect the information on title, last edited date, author, url for each article. It is strongly recommended NOT to use the code commercially without consent of Medici Media Co, Ltd!

# Prerequisites

    pip3 install requests
    pip3 install bs4

It could not matter what python version is, but it is recommended to use python 3.x (It might have been some issues using python 2.x)

# Cautions

Out of functions, update_article could be implemented but not perfectly. It means that you could utilize the function with some services which enable to automatically execute, for instance AWS Lambda.
