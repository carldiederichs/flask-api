import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://books.toscrape.com/'

page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")

bookshelf = soup.findAll("li",
                      {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

book_title_collection = []
for books in bookshelf: 
    book_title = books.h3.a['title']
    book_prices = soup.findAll('p', {'class':'price_color'})
    book_price = book_prices[0].text.strip()
    book_ratings = soup.findAll('p', {'class':'star-rating'})
    for book_rating in book_ratings:
        book_rating_stripped= book_rating.get('class')[1]
        if book_rating_stripped == "One":
            book_rating_stripped = 1
        elif book_rating_stripped == "Two":
            book_rating_stripped = 2
        elif book_rating_stripped == "Three":
            book_rating_stripped = 3
        elif book_rating_stripped == "Four":
            book_rating_stripped = 4
        elif book_rating_stripped == "Five":
            book_rating_stripped = 5
    case = {'title':book_title, 'price':book_price, 'rating': book_rating_stripped}
    book_title_collection.append(case)
json_string = json.dumps(book_title_collection)
print(json_string)

