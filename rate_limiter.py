from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta
from time import time

# initialises flask application
app = Flask(__name__)

# initializes RateLimiter class with time frame and request limit
class RateLimiter:
    def __init__(self, time_frame, limit_req):
        self.limit_req  = limit_req
        self.time_frame = time_frame
        self.users = {}
    
    # defines cases for allowed and declined requests
    def request_check(self, username, ip):
        self.t_now = datetime.now()
        username_ip = f'{username}:{ip}'
        
        # checks whether the username and ip combination is already stored in users dictionary and creates the key-value-pair if necessary
        if username_ip not in self.users: 
            self.users[username_ip] = {
                # 'ip_address': ip,
                # 'username': username,
                'req_count': 1, 
                'last_req_t': self.t_now,
            }
            return True
        
        # defines cases for user information already stored in users dictionary
        else: 
            self.user = self.users[username_ip]
            sec_since_last_req = (self.t_now - self.user['last_req_t']).total_seconds()
            
            # returns True if the time s passed ince the last request is greater than the limiting time frame, sets the request count to 1 and updates the timestamp 
            if sec_since_last_req > self.time_frame:
                self.user['req_count'] = 1
                self.user['last_req_t'] = self.t_now
                return True
            
            # returns True if user has made requests below the request limit, increments the request counter and updates the time stamp
            elif self.user['req_count'] < self.limit_req:
                self.user['req_count'] += 1
                self.user['last_req_t'] = self.t_now
                return True
            
            # returns False if user has made requests and request count is equal or greater to the limit
            else: 
                return False
    
    # retrieves user dict     
    def get_dict(self):
        return self.user