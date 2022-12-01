from flask import Flask
from flask import Flask, jsonify, request, send_file
from flask import request

app = Flask(__name__)

@app.route('/hello', methods = ['GET', 'POST'])
def welcome():
    return jsonify({'name':'Carl',
                    'message':'WELCOME TO MY API'}, 200)
    
@app.route('/numbers')
def print_numbers():
    return jsonify(list(range(5)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
    
data = request.data
print(data)
