from flask import Flask
from flask import Flask, jsonify, request, send_file
from flask import request
from bs4 import BeautifulSoup
import json
import requests

app = Flask(__name__)

BASE_URL = 'https://books.toscrape.com/'

page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")

books = soup.find_all('article')
book_information_scraped = []

@app.route('/book_info', methods = ['GET'])
def book_info():
    for book in books: 
        book_title = book.h3.a['title']
        book_price = book.find('p', class_='price_color').text
        book_rating = book.find('p', class_='star-rating').attrs.get('class')[1]
        case = {'title':book_title, 'price':book_price, 'rating': book_rating}
        book_information_scraped.append(case)
    return json.dumps(book_information_scraped)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
