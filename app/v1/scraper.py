import json, requests as rq
from bs4 import BeautifulSoup as bfs
from word2number import w2n
import uuid

class Scraper: 
    def __init__(self, num_pages=3):
        self.num_pages = num_pages
        self.book_information_scraped = []

    def scrape_books(self):
        page = 1
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
                self.book_information_scraped.append(case)
            page += 1

    def save_to_json(self, filename):
        with open(filename, 'w') as file_write: 
            json.dump(self.book_information_scraped, file_write, indent=4)
            
    def read_json_file(self, file_path, filename):
        with open(file_path, 'r') as file_read: 
            database = json.load(file_read)
            
        ids = [str(uuid.uuid4()) for _ in range(len(database))]
        database = [{**entry, 'id': id} for entry, id in zip(database, ids)]
        
        with open(filename, 'w') as f: 
            json.dump(database, f, indent=4)
            # return database
            