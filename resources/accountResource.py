from flask_restful import Resource
from flask import request
import json
import pyodbc

books = [{"id": 1, "title": "Java book"},
        {"id": 2, "title": "Python book"}]

server = '82.115.26.134'
database = 'ClimateWatch'
username = 'sa'
password = 'L(63luggHIkedq5>'
secret_key = 'your_secret_key'

def get_db_connection():
    return pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


class SignupPOSTResource(Resource):
    def post(self):
        data = request.get_json()
        full_name = data['full_name']
        username = data['username']
        password = data['password']
        telegram_id = data['telegram_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM Users WHERE UserName = ?", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 400

        # Insert user into database
        cursor.execute("INSERT INTO Users (FullName, UserName, Password, TelegramId) VALUES (?, ?, ?, ?)",
                   (full_name, username, password, telegram_id))
        conn.commit()

        conn.close()

        return jsonify({'message': 'User created successfully'}), 201
##############################################################333


