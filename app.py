from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Create DB connection
def create_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "sql12.freesqldatabase.com"),
        user=os.environ.get("DB_USER", "sql12779564"),
        password=os.environ.get("DB_PASS", "JPaK1tx39y"),
        database=os.environ.get("DB_NAME", "sql12779564")
    )

@app.route('/')
def home():
    return "✅ Flask + MySQL API running on Render"

@app.route('/users', methods=['GET'])
def get_users():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return jsonify(user) if user else ("User not found", 404)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "User created"}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (data['name'], data['email'], user_id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "User updated"})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
