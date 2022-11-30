from flask import Flask
from flask import Flask, jsonify, request, send_file

app = Flask()

@app.route('/my-flask-api', method = ['GET'])
def hello():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    
    
