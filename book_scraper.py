import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://books.toscrape.com/'

page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")

bookshelf = soup.findAll("li",
                         {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

book_title_collection = []
for books in bookshelf: 
    book_title = books.h3.a['title']
    book_price = books.div.p['price_color']
    book_title_collection.extend([book_title], [book_price])
print(book_title_collection)
    