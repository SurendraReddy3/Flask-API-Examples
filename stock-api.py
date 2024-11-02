from flask import Flask, request, jsonify
import boto3
from datetime import datetime

# Initialize the Flask app
app = Flask(_name_)

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'stock-user'
table = dynamodb.Table(table_name)

def create_order(order_id, script_code, price, order_type, profit_loss, LTP):
    """
    Inserts a new stock market order into the DynamoDB table.

    Parameters:
    - order_id (str): The unique ID for the order (Partition Key).
    - script_code (str): The code of the stock (Sort Key).
    - price (float): The price of the stock.
    - order_type (str): Type of order (e.g., buy or sell).
    - profit_loss (float): Profit or loss from the transaction.
    - LTP (float): Last Traded Price of the stock.

    Automatically adds created_date and modified_date.
    """
    
    current_date = datetime.now().isoformat()  # Current timestamp

    # Insert item into DynamoDB
    table.put_item(
        Item={
            'order_id': order_id,            # Partition Key (PK)
            'script_code': script_code,      # Sort Key (SK)
            'price': price,                  # Stock price
            'order_type': order_type,        # Buy or Sell
            'profit_loss': profit_loss,      # Profit or loss from the transaction
            'LTP': LTP,                      # Last traded price of the stock
            'created_date': current_date,    # Timestamp of creation
            'modified_date': current_date    # Timestamp of last modification
        }
    )
    return {'message': f"Order {order_id} for {script_code} created successfully."}

@app.route('/create_order', methods=['POST'])
def create_order_api():
    """
    API endpoint to create a new stock market order.
    """
    data = request.json
    required_fields = ['order_id', 'script_code', 'price', 'order_type', 'quantity', 'profit_loss', 'LTP']
    
    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    try:
        # Create the order by calling the helper function
        result = create_order(
            order_id=data['order_id'],
            script_code=data['script_code'],
            price=int(data['price']),
            order_type=data['order_type'],
            quantity=int(data['quantity']),
            profit_loss=int(data['profit_loss']),
            LTP=int(data['LTP'])
        )

        logging.info("info")
        # Return a success message
        return jsonify(result), 201

    except Exception as e:
        # Log the error with order_id and script_code context
        logging.error(f"Error placing order {data.get('order_id')} for {data.get('script_code')}: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/get_order', methods=['POST'])
def get_order():
    """
    API endpoint to retrieve a stock market order from DynamoDB.

    Expected POST data (JSON):
    - order_id: Unique ID of the order (Partition Key)
    - script_code: Stock code (Sort Key)

    Returns:
    - The order details if found, otherwise an error message.
    """
    
    # Parse the JSON data from the request
    data = request.json
    order_id = data.get('order_id')
    script_code = data.get('script_code')

    if not order_id or not script_code:
        return jsonify({'error': 'order_id and script_code are required'}), 400

    # Retrieve the item from DynamoDB
    response = table.get_item(
        Key={
            'order_id': order_id,
            'script_code': script_code
        }
    )
    
    # Check if the item exists
    item = response.get('Item')
    if not item:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(item), 200

# Run the Flask app
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5001, debug=True)