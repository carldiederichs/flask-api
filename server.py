import os
from flask import Flask, jsonify, request, send_file
from flask import request
from bs4 import BeautifulSoup as bfs
import json
import requests as rq
from word2number import w2n

app = Flask(__name__)

book_information_scraped = []
single_book_information = []

#assigns BASE_URL
BASE_URL = "https://books.toscrape.com"

@app.route('/', methods = ['GET'])
def index_get():
    return '<h1>Hello from Carl-Docker!</h1>'


#assigns flask endpoint
@app.route('/book_info', methods = ['GET'])

#retrieves all book info 
def book_info():
    page = 1
    
    #scrapes the first 5 pages
    while page <= 5:
        url = "https://books.toscrape.com/catalogue/page-{}.html".format(page)
        response = rq.get(url)
        page_content = bfs(response.content, 'html.parser')
        books = page_content.find_all('article')
        print(f'Now scraping page {page}')
        
        #retrieves book information for each page
        for book in books: 
            book_title = book.h3.a['title']
            book_price = book.find('p', class_='price_color').text
            book_rating = book.find('p', class_='star-rating').attrs.get('class')[1]
            book_rating_int = w2n.word_to_num(book_rating)
            case = {'title':book_title, 'price':book_price, 'rating': book_rating_int}
            book_information_scraped.append(case)
        page += 1
    return json.dumps(book_information_scraped)

#assigns flask endpoint
@app.route('/book_info_single/<title>', methods = ['GET', 'POST'])
def book_info_single(title):
    for book_details, book in enumerate(book_information_scraped):
        if book['title'] == title:
            return book_information_scraped[book_details]
    return "Invalid Title"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
