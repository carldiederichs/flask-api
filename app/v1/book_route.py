from flask import request, redirect, jsonify, render_template, redirect
from v1 import app
from v1.rate_limiter import RateLimiter
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

# assigns database file
database_file = 'v1/database.json'

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
        scrape.scrape_books()
        scrape.save_to_json(database_file)
        scrape.read_json_file(database_file, database_file)
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
    with open(database_file) as br: 
        books = json.load(br)
    return render_template('books.html', books=books)

# adds book
@app.route("/add_book", methods = ['GET','POST'])
def add_book():
    if request.method == 'GET':
        return render_template("add_book.html", book = {})
    if request.method == 'POST':
        id = request.form["id"]
        title = request.form["title"]
        rating = request.form["rating"]
        price = request.form["price"]
        with open(database_file) as br:
            books = json.load(br)
        books.append({"id": id, "title": title, "rating": rating, "price": price})
        with open(database_file, 'w') as bw:
            json.dump(books, bw, indent=4)
        return redirect('/all_books')
    
# updates book
@app.route('/update_book/<string:id>',methods = ['GET','POST'])
def update_book(id):
    with open(database_file) as br:
        books = json.load(br)
    if request.method == 'GET':
        book = [x for x in books if x['id'] == id][0]
        return render_template("add_book.html", book = book)
    if request.method == 'POST':
        for book in books:
            if(book['id'] == id):
                book['title'] = request.form["title"]
                book['rating'] = request.form["rating"]
                book['price'] = request.form["price"]
                break
        with open(database_file, 'w') as bw:
            json.dump(books, bw, indent=4)
        return redirect('/all_books')
    
# deletes book
@app.route('/delete_book/<string:id>')
def delete_book(id):
    with open(database_file) as br:
        books = json.load(br)
    newbooklist = []
    for book in books:
        if(book['id'] != id):
            newbooklist.append(book)
    with open(database_file, 'w') as bw:
        json.dump(newbooklist, bw, indent=4)
    return redirect('/all_books')