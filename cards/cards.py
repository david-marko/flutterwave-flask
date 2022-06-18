from flask import request, Blueprint, jsonify
from functions import db, dbname, get_token, get_user, login_required, fw_sec, wallet, xrate, clean
import requests, json
from dateutil import parser
cards = Blueprint('cards',__name__, url_prefix='/cards')

@cards.route('/')
@login_required
def checker():
    user_id = get_user()['id']
    # Check if card availalbe
    check = db("SELECT cards.card_id, cards.Status FROM `cards` WHERE `user_id` = "+str(user_id))
    if check:
        if check['Status'] == 1:
            header = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+fw_sec
            }
            r = requests.get('https://api.flutterwave.com/v3/virtual-cards/'+check['card_id'], headers=header)
            res = json.loads(r.content)
            amount = res['amount']
            return jsonify({'status':'success', 'amount': amount })
        else:
            return jsonify({'status':'success','message':'Your Card will be ready shortly'})
    else:
        return jsonify({'status':'error','message':'Please Request for a virtual card'})

@cards.route('/add')
@login_required
def add():
    my_user = get_user()
    user_id = my_user['id']
    check = db("SELECT cards.card_id, cards.Status FROM `cards` WHERE `user_id` = "+str(user_id))
    if check:
        return jsonify({'status':'error', 'message':'You can only have on virtual card'})
    else:
        balance = wallet(user_id)
        if my_user['Currency'] == 'USD':
            if balance > 25:
                db("INSERT INTO `cards` (`id`, `user_id`, `card_id`, `Created`, `Status`) VALUES (NULL, '"+user_id+"', '', current_timestamp(), '0');",'insert')
                sql = "INSERT INTO `billing` (`id`, `user_id`, `Kind`, `merch_id`, `Amount`, `Conv_amount`, `Currency`, `Gateway`, `txref`, `Created`, `Confirmed`, `Comments`, `Details`, `Status`) VALUES (NULL, '"+user_id+"', 'SUB', '1', '25', '25', 'USD', 'SYSTEM', '', current_timestamp(), current_timestamp(), 'Card Creation', '', '1');"
                db(sql,'insert')
                return jsonify({'status':'success','message':'Virtual Card is currently being created. You will be notified shortly'})
            else:
                return jsonify({'status':'error','message':'Insufficient Balance to get a Card'})
        elif my_user['Currency'] == 'SSP':
            if balance > xrate(25,'USD','SSP'):
                db("INSERT INTO `cards` (`id`, `user_id`, `card_id`, `Created`, `Status`) VALUES (NULL, '"+user_id+"', '', current_timestamp(), '0');",'insert')
                sql = "INSERT INTO `billing` (`id`, `user_id`, `Kind`, `merch_id`, `Amount`, `Conv_amount`, `Currency`, `Gateway`, `txref`, `Created`, `Confirmed`, `Comments`, `Details`, `Status`) VALUES (NULL, '"+user_id+"', 'SUB', '1', '25', '"+str(xrate(25,'USD','SSP'))+"', 'SSP', 'SYSTEM', '', current_timestamp(), current_timestamp(), 'Card Creation', '', '1');"
                db(sql,'insert')
                return jsonify({'status':'success','message':'Virtual Card is currently being created. You will be notified shortly'})
            else:
                return jsonify({'status':'error','message':'Insufficient Balance to get a Card'})

@cards.route('/topup', methods=['POST'])
@login_required
def topup():
    my_user = get_user()
    currency = my_user['Currency']
    user_id = my_user['id']
    if request.method == 'POST':
        amount = clean(request.form['amount'])
        if currency == 'USD':
            sql = "INSERT INTO `billing` (`id`, `user_id`, `Kind`, `merch_id`, `Amount`, `Conv_amount`, `Currency`, `Gateway`, `txref`, `Created`, `Confirmed`, `Comments`, `Details`, `Status`) VALUES (NULL, '"+user_id+"', 'SUB', '1', '"+amount+"', '"+amount+"', 'USD', 'SYSTEM', '', current_timestamp(), current_timestamp(), 'Card Creation', '', '1');"
            db(sql,'insert')
        else:
            sql = "INSERT INTO `billing` (`id`, `user_id`, `Kind`, `merch_id`, `Amount`, `Conv_amount`, `Currency`, `Gateway`, `txref`, `Created`, `Confirmed`, `Comments`, `Details`, `Status`) VALUES (NULL, '"+user_id+"', 'SUB', '1', '"+amount+"', '"+str(xrate(amount,'SSP','USD'))+"', 'SSP', 'SYSTEM', '', current_timestamp(), current_timestamp(), 'Card Creation', '', '1');"
            db(sql,'insert')
        # Check if flw can top up balance directly

@cards.route('/view/<string:card_id>')
@login_required
def view(card_id):
    user_id = get_user()['id']
    check = db("SELECT * FROM `cards` WHERE `user_id` = "+user_id+" AND `card_id` = '"+clean(card_id)+"'")
    if check:
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+fw_sec
        }
        r = requests.get('https://api.flutterwave.com/v3/virtual-cards/'+card_id, headers=header)
        res = json.loads(r.content)
        pan = res['data']['card_pan']
        n = 4
        spliter = [pan[i:i+n] for i in range(0, len(pan), n)]
        masked = ''
        for each in spliter:
            masked += each+' '
        res['data']['card_pan'] = masked
        res['data']['expiration'] = res['data']['expiration'][-2:]+'/'+res['data']['expiration'][:4]
        created = parser.parse(res['data']['created_at'])
        res['data']['created_at'] = created.strftime('%d/%m/%Y')
        r2 = requests.get('https://api.flutterwave.com/v3/virtual-cards/'+card_id+'/transactions?from=2019-01-01&to=2022-04-04&index=0&size=10', headers=header)
        res2 = json.loads(r2.content)
        return jsonify({'status':'successs','card': res,'transactions': res2['data']})
    else:
        return jsonify({'status':'error','message':'Not Authorized'})