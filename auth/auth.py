from flask import Blueprint, jsonify, request
from functions import db, dbname, clean, set_token

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = clean(request.form['email'])
        password = clean(request.form['password'])
        check = db("SELECT users.id, `f_name`, `l_name`, `Phone`, `Currency`, `Status` FROM `users` WHERE `Email` = '"+email+"' AND `Password` = '"+password+"'")
        if check:
            profile = {}
            profile['first_name'] = check['f_name']
            profile['last_name'] = check['last_name']
            profile['phone'] = check['Phone']
            profile['currency'] = check['Currency']
            profile['status'] = check['Status']
            return jsonify({'status':'success','token':set_token(check['id']), 'profile': profile})
        else:
            return jsonify({'status':'error','message':'Invalid Login Credentials'})

@auth.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = clean(request.form['email'])
        password = clean(request.form['password'])
        f_name = clean(request.form['f_name'])
        l_name = clean(request.form['l_name'])
        phone = clean(request.form['phone'])
        currency = clean(request.form['currency'])
        referal = clean(request.form['referal'])
        check = db("SELECT * FROM `users` WHERE `Email` = '"+email+"' OR `Phone` = '"+phone+"'")
        if check:
            return jsonify({'status':'error', 'message':'A similar account already exists. Please login instead'})
        else:
            sql = "INSERT INTO `users` (`id`, `Email`, `Password`, `f_name`, `l_name`, `Phone`, `Currency`, `OTP`, `Created`, `Comment`, `Status`) VALUES (NULL, '"+email+"', '"+password+"', '"+f_name+"', '"+l_name+"', '"+phone+"', '"+currency+"', NULL, current_timestamp(), '"+referal+"', '1');"
            token = db(sql,'insert')
            # Check if referal available and reward a user
            return jsonify({'status':'success', 'token': set_token(token)})

@auth.route('/forgot', methods=['POST'])
def forgot():
    # After configuring sendgrid
    pass