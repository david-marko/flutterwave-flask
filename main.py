from flask import Flask, jsonify
from flask_cors import CORS
from auth.auth import auth
from cards.cards import cards

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(cards)

CORS(app)
app.secret_key = 'testtest'

@app.route('/')
def hello():
    return jsonify({'status':'success', 'message':'API'})

if __name__ == '__main__':
    app.run(debug=True)