from flask import Flask, request, Response, redirect, jsonify, render_template, url_for, flash, redirect
from v1 import app
from v1.rate_limiter import RateLimiter
from v1.forms import RegistrationForm, LoginForm
from v1.book_model import User, Book
from v1.scraper import Scraper
from datetime import timedelta
import json

# assigns BASE_URL
BASE_URL = "https://books.toscrape.com"

# allows configurable invocations to the reseouce within a given time window
time_limit = 30
request_limit = 2

# assigns rate limit to the Rate Limiter class with time limit and request limit as input arguments
rate_limit = RateLimiter(time_limit, request_limit) 
scrape = Scraper()

#-----Flask Endpoints--------------------------------------------------------------------------------------------------------

# sets route for index page
@app.route('/')
def index_get():
    return '<h1>Welcome to my library!</h1>'

# # connects to books Flask endpoint allowing a get request to retrieve book information from the self-created API
@app.route('/books', methods=['GET'])
# runs rate limiter to check the amount of requests in a given time frame 
def books():
    
    # requests headers ip_address and username
    ip_address = request.headers.get('ip', request.remote_addr)
    username = request.headers.get("username") # -> Only executes if user logged in

    # calls request_check method in the rate_limit object and returns the all_books function if request is allowed
    if rate_limit.request_check(username, ip_address):
        return all_books()
    
    # updates last request time in the rate limiter dictionary if the request fails and displays error message
    else:
        user_dict = rate_limit.get_dict()
        next_access_t = (user_dict['last_req_t'] + timedelta(seconds=time_limit)).strftime("%m/%d/%Y, %H:%M:%S")
        error_message = f"Sorry, there were too many requests! Please try again at {next_access_t}. You only have {request_limit} requests per {time_limit} seconds."
        return jsonify({'Error 429': error_message}), 429

# assigns flask endpoint for all book info 
@app.route('/all_books', methods = ['GET'])

# retrieves all books 
def all_books():
    scrape.scrape_books()
    scrape.save_to_json('v1/database.json')
    return scrape.read_json_file('v1/database.json', 'v1/database.json')

@app.route('/book/new')
# @login_required
def create_book():
    return render_template('create_book.html', title='New Book')