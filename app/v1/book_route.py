from flask import Flask, request, Response, redirect, jsonify, render_template, url_for, flash, redirect
from v1 import app
from v1.rate_limiter import RateLimiter
from v1.forms import RegistrationForm, LoginForm
from v1.book_model import User, Book
from datetime import timedelta
from word2number import w2n
from bs4 import BeautifulSoup as bfs
import json, requests as rq

# creates lists for book information
book_information_scraped = []
single_book_information = []

# tracks previous requests
prev_req = {}

# assigns BASE_URL
BASE_URL = "https://books.toscrape.com"

# RATE LIMITER

# allows configurable invocations to the reseouce within a given time window
time_limit = 30
request_limit = 2

# assigns rate limit to the Rate Limiter class with time limit and request limit as input arguments
rate_limit = RateLimiter(time_limit, request_limit) 

#-----Flask Endpoints--------------------------------------------------------------------------------------------------------

# sets route for index page
@app.route('/')
def index_get():
    return '<h1>Welcome to my library!</h1>'

# # connects to get_info Flask endpoint allowing a get request to retrieve book information from the self-created API
@app.route('/get_info', methods=['GET'])
# runs rate limiter to check the amount of requests in a given time frame 
def get_info():
    
    # requests headers ip_address and username
    ip_address = request.headers.get('ip', request.remote_addr)
    username = request.headers.get("username") # -> Only executes if user logged in

    # calls request_check method in the rate_limit object and returns the book_info function if request is allowed
    if rate_limit.request_check(username, ip_address):
        return book_info()
    
    # updates last request time in the rate limiter dictionary if the request fails and displays error message
    else:
        user_dict = rate_limit.get_dict()
        next_access_t = (user_dict['last_req_t'] + timedelta(seconds=time_limit)).strftime("%m/%d/%Y, %H:%M:%S")
        error_message = f"Sorry, there were too many requests! Please try again at {next_access_t}. You only have {request_limit} requests per {time_limit} seconds."
        return jsonify({'Error 429': error_message}), 429

# assigns flask endpoint for all book info 
@app.route('/book_info', methods = ['GET'])
# @rate_limiter

# retrieves all book info 
def book_info():
    page = 1
    
    # scrapes the first 3 pages
    while page <= 3:
        url = "https://books.toscrape.com/catalogue/page-{}.html".format(page)
        response = rq.get(url)
        page_content = bfs(response.content, 'html.parser')
        books = page_content.find_all('article')
        print(f'Now scraping page {page}')
        
        # retrieves book information for each page
        for book in books: 
            book_title = book.h3.a['title']
            book_price = book.find('p', class_='price_color').text
            book_rating = book.find('p', class_='star-rating').attrs.get('class')[1]
            book_rating_int = w2n.word_to_num(book_rating)
            case = {'title': book_title, 'price': book_price, 'rating': book_rating_int}
            book_information_scraped.append(case)
        page += 1
    return json.dumps(book_information_scraped)

# assigns flask endpoint for single book
@app.route('/book_info/<title>', methods = ['GET', 'POST'])
def book_info_single(title):
    for book_details, book in enumerate(book_information_scraped):
        if book['title'] == title:
            return book_information_scraped[book_details]
    return "Invalid Title"