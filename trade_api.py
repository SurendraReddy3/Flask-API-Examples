from flask import Flask,request, jsonify
import boto3
from datetime import datetime
import logging

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
users = dynamodb.Table("user_table")
trades = dynamodb.Table("trade_table")

@app.route('/create_user', methods =['POST'])
def create_user():
    data = request.json
    required_fields = ['user_id', 'email_address','password']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
        
    try:
        current_date = datetime.now().isoformat()

        users.put_item(
            Item={
                'user_id': data['user_id'],
                'email_address': data['email_address'],
                'password': data['password'],
                'created_date': current_date,
                'modified_date': current_date
            }
        )

        logging.info(f"User {data['user_id']} created Successfully")
        return jsonify({'message': f"User {data['user_id']} created Successfully"}), 201
    
    except Exception as e:
        logging.error(f"Error creating user {data.get('user_id')}: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/create_trade', methods=['POST'])   
def create_order():
    data = request.json
    required_fields = ['order_id','user_id', 'script_code', 'order_type', 'price', 'ltp', 'quantity', 'profit_loss']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
        
    try:
        current_date = datetime.now().isoformat()

        trades.put_item(
            Item = {
                'order_id': data['order_id'],
                'user_id': data['user_id'],
                'script_code': data['script_code'],
                'order_type': data['order_type'],
                'price': data['price'],
                'ltp': data['ltp'],
                'quantity': data['quantity'],
                'profit_loss': data['profit_loss'],
                'create_date': current_date,
                'modified_date': current_date
            }
        )

        logging.info(f"Order {data['order_id']} script_code {data['script_code']} created successfully")
        return jsonify({'message': f"Order {data['order_id']}, {data['script_code']} created successfully"}), 201
    
    except Exception as e:
        logging.error(f"Error creating_order {data.get['order_id']}: {e}")
        return jsonify({'error':str(e)}), 500

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

    

    
     


    


