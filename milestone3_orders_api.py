from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'ecommerce.db'  # adjust if yours is named differently

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows dictionary-like row access
    return conn

@app.route('/api/customers/<int:customer_id>/orders', methods=['GET'])
def get_orders_for_customer(customer_id):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM users WHERE id = ?', (customer_id,)).fetchone()

    if customer is None:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    orders = conn.execute('SELECT * FROM orders WHERE user_id = ?', (customer_id,)).fetchall()
    conn.close()

    return jsonify({
        'customer': dict(customer),
        'orders': [dict(order) for order in orders]
    }), 200

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,)).fetchone()
    conn.close()

    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(dict(order)), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
