from flask import Flask,jsonify
import boto3
import logging
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, methods=["GET", "POST", "OPTIONS"], allow_headers=["Authorization", "Content-Type"])

dynamodb = boto3.resource('dynamodb',region_name = 'ap-south-1')
login_table = dynamodb.Table("login_user")

@app.route('/getallusers', methods=['GET'])
@cross_origin(origins='*')
def get_all_users():
    try:
        response = login_table.scan()
        users = response.get('Items',[])

        if users:
            logging.info("Retrieved all user information")
            return jsonify(users), 200
        else:
            logging.info("No users found")
            return jsonify({"message":"no users found"}), 404
    except Exception as e:
        logging.error(f"error retrieving all users: {e}")
        return jsonify({'error':str(e)}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)