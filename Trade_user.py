from flask import Flask, request, jsonify
import boto3
from datetime import datetime

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'Trade_user'
table = dynamodb.Table(table_name)

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    
    # Extract required fields from the request
    script_id = data.get('script_id')
    resource_id = data.get('resource_id')  # Assuming this is the token with resource_id and username
    order_type = data.get('order_type')  # Buy or Sell
    quantity = int(data.get('quantity')) if 'quantity' in data else None
    purchase_price = int(data.get('purchase_price'))  # for float error was rising so that’s why int was used
    ltp = float(data.get('ltp')) if 'ltp' in data else None  # Corrected 'itp' to 'ltp'
    created_date = datetime.utcnow()  # First-time created date
    modified_date = datetime.utcnow()  # Current modified date using UTC
    modified_by = 1
    created_by = 1
    order_id = data.get('order_id')
    
    # Validate required fields
    if not all([script_id, order_type, quantity, purchase_price, ltp, order_id]):
        return jsonify({'error': 'All required fields must be provided'}), 400

    if order_type not in ['Buy', 'Sell']:
        return jsonify({'error': 'Invalid order_type. Only "Buy" or "Sell" is allowed'}), 400

    if order_type == 'Buy':
        table.put_item(
            Item={
                'order_id': order_id,  # Partition Key (PK)
                'script_id': script_id,  # Sort Key (SK)
                'quantity': quantity,  # Number of stocks bought
                'purchase_price': purchase_price,  # Purchase price per stock
                'ltp': ltp,  # Last Traded Price
                'created_date': created_date,  # First-time created date
                'modified_date': modified_date,  # Last modified date
                'created_by': created_by,  # User who created the order
                'modified_by': modified_by,  # User who modified the order
            }
        )
        return jsonify({'message': f"Buy order {order_id} for {quantity} stocks of {script_id} created successfully."}), 201

    elif order_type == 'Sell':
        # Try to retrieve the buy order details
        try:
            response = table.get_item(
                Key={
                    'order_id': order_id,
                    'script_id': script_id
                }
            )
            order = response.get('Item')

            if not order:
                return jsonify({'error': 'Buy order not found'}), 404

            available_quantity = order['quantity']
            if available_quantity < quantity:
                return jsonify({'error': 'Not enough stocks to sell'}), 400

            # Update the remaining quantity after selling
            remaining_quantity = available_quantity - quantity

            # Calculate total sale amount
            sale_amount = quantity * ltp  # Sell quantity * Last Traded Price (ltp)

            # If remaining quantity is zero, delete the record
            if remaining_quantity == 0:
                table.delete_item(
                    Key={
                        'order_id': order_id,
                        'script_id': script_id
                    }
                )
            else:
                # Otherwise, update the remaining quantity
                table.update_item(
                    Key={
                        'order_id': order_id,
                        'script_id': script_id
                    },
                    UpdateExpression="SET quantity = :q, modified_date = :m",
                    ExpressionAttributeValues={
                        ':q': remaining_quantity,
                        ':m': modified_date
                    }
                )

            return jsonify({
                "status": "success",
                "message": f"Sold {quantity} stocks of {script_id} at price {ltp} successfully.",
                "remaining_quantity": remaining_quantity,
                "sale_amount": sale_amount,
                "code": 200
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
