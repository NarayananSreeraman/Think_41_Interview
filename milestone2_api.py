from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
DATABASE = 'ecommerce.db'
CORS(app)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So we can get dict-like rows
    return conn

@app.route('/customers', methods=['GET'])
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM users LIMIT ? OFFSET ?', (limit, offset)).fetchall()
    conn.close()

    result = [dict(row) for row in customers]
    return jsonify(result), 200

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM users WHERE id = ?', (customer_id,)).fetchone()

    if customer is None:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    order_count = conn.execute('SELECT COUNT(*) FROM orders WHERE user_id = ?', (customer_id,)).fetchone()[0]
    conn.close()

    customer_data = dict(customer)
    customer_data['order_count'] = order_count

    return jsonify(customer_data), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
