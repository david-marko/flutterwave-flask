from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'codemode'

@app.route('/')
def hello():
    return jsonify({'status':'success', 'message':'API'})

if __name__ == '__main__':
    app.run(debug=True)