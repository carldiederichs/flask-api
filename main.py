from flask import Flask
from flask import Flask, jsonify, request, send_file
from flask import request
from bs4 import BeautifulSoup
import json
import requests
from word2number import w2n
import eel
import webbrowser
from threading import Timer


app = Flask(__name__)

BASE_URL = 'https://books.toscrape.com/'

page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")

books = soup.find_all('article')
book_information_scraped = []
single_book_information = []

@app.route('/book_info', methods = ['GET'])
def book_info():
    for book in books: 
        book_title = book.h3.a['title']
        book_price = book.find('p', class_='price_color').text
        book_rating = book.find('p', class_='star-rating').attrs.get('class')[1]
        book_rating_int = w2n.word_to_num(book_rating)
        case = {'title':book_title, 'price':book_price, 'rating': book_rating_int}
        book_information_scraped.append(case)
    return json.dumps(book_information_scraped)

@app.route('/book_info_single/<title>', methods = ['GET', 'POST'])
def book_info_single(title):
    for i, book in enumerate(book_information_scraped):
        if book['title'] == title:
            return book_information_scraped[i]
    return "Invalid Title"

def open_browser():
      webbrowser.open_new("http://127.0.0.1:8000/book_info")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(port=8000)