from flask import Flask, redirect, request, jsonify, make_response, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, json
from hashids import Hashids
import datetime
from functools import wraps
import jwt, math

from werkzeug.wrappers import response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)


with open('config.JSON') as config_file:
    config = json.load(config_file)

app.config['SECRET_KEY'] = config['app_secret']

dbhost = config['database']['host']
dbuser = config['database']['user']
dbpass = config['database']['password']
dbname = config['database']['database']

hashkey = config['hashing']['key']
authsize = 16
salt = config['hashing']['salt']

fw_pub = config['flutterwave']['pub_key']
fw_sec = config['flutterwave']['sec_key']

# flutter_pub = config['flutterwave']['pub']
# flutter_sec = config['flutterwave']['sec']

# sgkey = config['sendgrid']['key']

def send_mail(destination, subject, body):
    maessage = Mail(
        from_email='mailuser',
        to_emails=destination,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient('sgkey')
        response = sg.send(maessage)
        print(response.status_code)
        return True
    except Exception as e:
        print(e.message)
        return False

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def set_token(string,authsize=authsize):
    hashid = Hashids(salt="this_is_the_salt", min_length=authsize)
    return hashid.encode(string)

def get_token(string,authsize=authsize):
    hashid = Hashids(salt="this_is_the_salt", min_length=authsize)
    ret = hashid.decode(string)[0]
    return str(ret)

def create_hash(id):
    hashid = Hashids(salt="this_is_the_salt", min_length=authsize)
    return hashid.encode(id)

def decode_hash(id):
    hashids = Hashids(min_length=authsize, salt="this_is_the_salt")
    id = hashids.decode(id)
    return str(id[0])

def db(sql, query='select'):
    conn = mysql.connector.connect(host=dbhost,user=dbuser,port=3306, password=dbpass,database=dbname)
    cursor = conn.cursor(dictionary=True,buffered=True)
    ret = []
    # sql = conn.converter.escape(sql)
    cursor.execute(sql)
    if query == 'select':
        ret = cursor.fetchone()
    elif query == 'many':
        ret = cursor.fetchall()
    elif query == 'insert':
        ret = cursor.lastrowid
        conn.commit()
    elif query == 'update':
        conn.commit()
        ret = True
    cursor.close()
    return ret

def clean(strings):
    conn = mysql.connector.connect(host=dbhost,user=dbuser, password=dbpass,database=dbname)
    return conn.converter.escape(strings)


def xrate(amount, first, last ):
    rate = db("SELECT xrate.amount FROM `xrate` WHERE xrate.from_cur = '"+first+"' AND xrate.to_cur = '"+last+"' ORDER BY xrate.id DESC")['amount']
    if (last != 'SSP'):
        final_balance = int(math.ceil(rate * amount*1.03))
    else:
        final_balance = int(math.ceil(rate * amount))
    return final_balance

def get_balance(user_id, merch_id, currency=False):
    currencies = ['USD','SSP','UGX','KES']
    if currency == False:
        wallet = {}
        for each in currencies:
            credit = db("SELECT SUM(`Amount`) as 'Credit' FROM `withdraw` WHERE withdraw.Currency = '"+each+"' AND `user_id` = "+user_id+" AND `merch_id` = "+merch_id)
            if not credit or credit['Credit'] is None:
                credit = 0
            else:
                credit = credit['Credit']
            debit = db("SELECT SUM(`Amount`) as 'Debit' FROM `collect` WHERE `merch_id` = "+merch_id+" AND `Status` = 1 AND `Currency` = '"+each+"';")
            if not debit or debit['Debit'] is None:
                debit = 0
            else:
                debit = debit['Debit']
            balance = debit-credit
            wallet[each] = balance
        return wallet
    else:
        credit = db("SELECT SUM(`Amount`) as 'Credit' FROM `withdraw` WHERE withdraw.Currency = '"+currency+"' AND `user_id` = "+user_id+" AND `merch_id` = "+merch_id)
        if not credit or credit['Credit'] is None:
            credit = 0
        else:
            credit = credit['Credit']
        debit = db("SELECT SUM(`Amount`) as 'Debit' FROM `collect` WHERE `merch_id` = "+merch_id+" AND `Status` = 1 AND `Currency` = '"+currency+"';")
        if not debit or debit['Debit'] is None:
            debit = 0
        else:
            debit = debit['Debit']
        balance = float(debit-credit)
        return balance

def wallet(id):
    user_id = str(id)
    added = db("SELECT SUM(`Conv_amount`) as 'Added' FROM `billing` WHERE `user_id` = "+user_id+" AND `Kind` = 'ADD';")
    if not added:
        added = 0
    sub = db("SELECT SUM(`Conv_amount`) as 'Added' FROM `billing` WHERE `user_id` = "+user_id+" AND `Kind` = 'SUB';")
    if not sub:
        sub = 0
    wallet = float(added - sub)
    return wallet
    
def get_user():
    token = request.headers['x-access-tokens']
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    current_user = db("SELECT * FROM "+dbname+".users WHERE users.id = "+str(data['public_id']))
    if not current_user:
        return jsonify({'status':'error', 'message': 'invalid token used'})
    else:
        return current_user    

def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'status':'error', 'message':'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = db("SELECT * FROM "+dbname+".users WHERE users.id = "+str(data['public_id']))
            if not current_user:
                return jsonify({'status':'error', 'message': 'invalid token used'})
        except:
            return jsonify({'status':'error','message': 'token is invalid'})
        return f(*args, **kwargs)
    return decorator