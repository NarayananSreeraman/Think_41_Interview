import sqlite3
import pandas as pd

# Load CSV files
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')

# Connect to SQLite DB (creates a file if not exists)
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Drop tables if they exist
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS orders")

# Create 'users' table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)
''')

# Create 'orders' table
cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product TEXT,
    amount REAL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Load data into tables
users_df.to_sql('users', conn, if_exists='append', index=False)
orders_df.to_sql('orders', conn, if_exists='append', index=False)

# Verify data loaded
print("Users:")
for row in cursor.execute("SELECT * FROM users LIMIT 5"):
    print(row)

print("\nOrders:")
for row in cursor.execute("SELECT * FROM orders LIMIT 5"):
    print(row)

# Commit and close connection
conn.commit()
conn.close()
