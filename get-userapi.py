from flask import Flask,jsonify
import boto3
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
login_table = dynamodb.Table("login_user")

@app.route('/get-user/<username>', methods=['GET'])
def get_user(username):
    try:
        # Fetch the user from DynamoDB using only the partition key
        response = login_table.get_item(Key={'username': username})

        # Check if the user exists
        if 'Item' in response:
            user_data = response['Item']
            logging.info(f"Retrieved user information for: {username}")
            return jsonify({
                "username": user_data['username'],
                "password": user_data['password'],
                "status":user_data.get('status','unknown')
            }), 200
        else:
            logging.info(f"User not found: {username}")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving user {username}: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="127.0.0.1",port="5001",debug=True)