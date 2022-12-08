from flask import Flask
from flask import Flask, jsonify, request, send_file
from flask import request
from bs4 import BeautifulSoup as bfs
import json
import requests as rq
from word2number import w2n
import webbrowser
from threading import Timer
import time

app = Flask(__name__)

book_information_scraped = []
single_book_information = []

@app.route('/book_info', methods = ['GET'])
def book_info():
    page = 1
    while page <= 50:
        url = "https://books.toscrape.com/catalogue/page-{}.html".format(page)
        response = rq.get(url)
        page_content = bfs(response.content, 'html.parser')
        books = page_content.find_all('article')
        print(f'Now scraping page {page}')
        
        for book in books: 
            book_title = book.h3.a['title']
            book_price = book.find('p', class_='price_color').text
            book_rating = book.find('p', class_='star-rating').attrs.get('class')[1]
            book_rating_int = w2n.word_to_num(book_rating)
            case = {'title':book_title, 'price':book_price, 'rating': book_rating_int}
            book_information_scraped.append(case)
        page += 1
        time.sleep(2)
    return json.dumps(book_information_scraped)

@app.route('/book_info_single/<title>', methods = ['GET', 'POST'])
def book_info_single(title):
    for book_details, book in enumerate(book_information_scraped):
        if book['title'] == title:
            return book_information_scraped[book_details]
    return "Invalid Title"

def open_browser():
      webbrowser.open_new("http://127.0.0.1:8000/book_info")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(port=8000)