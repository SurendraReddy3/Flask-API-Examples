from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import jwt
import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'ameetparse'

# In-memory user storage (simulating a database)
users = {}

# Helper function to generate JWT token
def generate_token(user_name):
    token = jwt.encode({
        'user_name': user_name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Register User API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() # Get the JSON from the Request Body

    # Get the User Sign in data from the payload
    user_name = data['user_name']
    email_address = data['email_address']
    phone_number = data['phone_number']
    address = data['address']
    password = data['password']

    if user_name in users:
        return jsonify({'message': 'User already exists', "Code" : "1001"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users[user_name] = {
        'user_name': user_name,
        'email_address': email_address,
        'phone_number': phone_number,
        'address': address,
        'password': hashed_password
    }

    # Get the Token for the user based on the {user_name} 
    token = generate_token(user_name)
    
    # Build or Prepare the Response 
    response = {
        'user_name': user_name,
        'email_address': email_address,
        'phone_number': phone_number,
        'address': address,
        'token': token
    }
    return jsonify(response), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email_address = data['email_address']
    password = data['password']

    user = users.get(email_address)

    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = generate_token(user['user_name'])
    return jsonify({'token': token}), 200

# Forget Password API
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email_address = data['email_address']

    user = users.get(email_address)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # In a real-world app, send a password reset email or SMS here
    return jsonify({'message': 'Password reset instructions sent'}), 200

# Change Password API
@app.route('/change_password', methods=['PUT'])
def change_password():
    data = request.get_json()
    email_address = data['email_address']
    old_password = data['old_password']
    new_password = data['new_password']
    token = data['token']

    # Get the Tocken
    # Decrypt Token 
    # if Token is Good then proceed with Update else access denined

    user = users.get(email_address)

    if not user or not bcrypt.check_password_hash(user['password'], old_password):
        return jsonify({'message': 'Invalid credentials'}), 401

    users[email_address]['password'] = bcrypt.generate_password_hash(new_password).decode('utf-8')
    return jsonify({'message': 'Password updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
