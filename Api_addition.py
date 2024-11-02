# pip install Flask
# python app.py
# curl -X POST http://localhost:5000/add -H "Content-Type: application/json" -d '{"first_number": 10, "second_number": 20}'

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.json
    first_number = data.get('first_number')
    second_number = data.get('second_number')

    if first_number is None or second_number is None:
        return jsonify({"error": "ENter both numbers"}), 400

    try:
        sum_result = float(first_number) + float(second_number)
    except ValueError:
        return jsonify({"error": "Invalid numbers provided"}), 400

    return jsonify({"sum": sum_result})

@app.route('/sub', methods=['POST'])
def substract():
    data = request.json
    first_number = data.get('first_number')
    second_number = data.get('second_number')

    if first_number is None or second_number is None:
        return jsonify({"error": "ENter both numbers"}), 400

    try:
        sum_result = float(first_number) - float(second_number)
    except ValueError:
        return jsonify({"error": "Invalid numbers provided"}), 400

    return jsonify({"subraction": sum_result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

