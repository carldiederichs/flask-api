import requests
from bs4 import BeautifulSoup
import json
from word2number import w2n

BASE_URL = 'https://books.toscrape.com/'

page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")

books = soup.find_all('article')
book_information_scraped = []

for book in books: 
    book_title = book.h3.a['title']
    book_price = book.find('p', class_='price_color').text
    book_rating = book.find('p', class_='star-rating').attrs.get('class')[1]
    case = {'title':book_title, 'price':book_price, 'rating': book_rating}
    book_information_scraped.append(case)
json_string = json.dumps(book_information_scraped)
print(json_string)