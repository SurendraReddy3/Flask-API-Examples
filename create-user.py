from flask import Flask, request, jsonify
import boto3
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'user-master'
table = dynamodb.Table(table_name)

def create_user(email_address, user_id, full_name, token, resourceid, status):
    """
    Inserts a new user record into the DynamoDB table.

    Parameters:
    - email_address (str): The email address of the user (Primary Key).
    - user_id (str): A unique identifier for the user (Sort Key).
    - full_name (str): The full name of the user.
    - token (str): JWT token for authentication.
    - resourceid (str): Unique ID for resources linked to the user.
    - status (str): Status of the user (e.g., active/inactive).

    Automatically adds `created_date` and `modified_date`.
    """
    
    current_date = datetime.now().isoformat()  # Current timestamp

    # Insert item into DynamoDB
    table.put_item(
        Item={
            'email_address': email_address,  # Partition Key (PK)
            'user_id': user_id,              # Sort Key (SK)
            'full_name': full_name,          # User's full name
            'token': token,                  # JWT token for authentication
            'resourceid': resourceid,        # Resource ID linked to the user
            'created_date': current_date,    # Timestamp of creation
            'modified_date': current_date,   # Timestamp of last modification
            'status': status,                 # Status (active/inactive)
            'Test':'Voonna'
        }
    )
    return {'message': f"User {email_address} created successfully."}

@app.route('/create_user', methods=['POST'])
def create_user_api():
    """
    API endpoint to create a new user in the DynamoDB table.

    Expected POST data (JSON):
    - email_address: User's email (Primary Key)
    - user_id: User's unique ID (Sort Key)
    - full_name: Full name of the user
    - token: JWT token for authentication
    - resourceid: Resource ID linked to the user
    - status: User's status (e.g., active/inactive)

    Returns:
    - Success message if the user is created.
    """
    
    # Parse the JSON data from the request
    data = request.json

    # Check if all required fields are present
    required_fields = ['email_address', 'user_id', 'full_name', 'token', 'resourceid', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Create the user by calling the helper function
    result = create_user(
        email_address=data['email_address'],
        user_id=data['user_id'],
        full_name=data['full_name'],
        token=data['token'],
        resourceid=data['resourceid'],
        status=data['status']
    )

    # Return a success message
    return jsonify(result), 201

@app.route('/get_user', methods=['POST'])
def get_user():
    data=request.get_json
    email_address=data['email_address']
    user_id=data['user_id']
    response = table.get_item(
        Key={
            'email_address': email_address,
            'user_id': user_id
        }
    )
    return response.get('Item')

# Example usage
user = get_user('test@example.com', '123')
print(user)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
