from flask_restful import Resource
from flask import request
import json
import pyodbc

from influxdb import InfluxDBClient

from datetime import datetime


# Set the InfluxDB connection parameters
host = '68.183.12.39'  # replace with your InfluxDB hostname or IP address
port = 8086  # default port for InfluxDB
username = 'your_username'  # replace with your username
password = 'your_password'  # replace with your password
database = 'CW'  # replace with your database name

# Create client
client = InfluxDBClient(host=host, port=port, database=database)

#########################################################

class MeasurementPOSTResource(Resource):
    def post(self):
        data = request.get_json()
        json_body = data['measurement']
        client.write_points(json_body)


        client.close()

        return 'New data inserted', 201
    

class MeasurementsGETResource(Resource):
    def get(self):
        query = 'SELECT * FROM sensor_data'
        result = client.query(query)
        measurements = result.get_points()


        user_list = []
        for point in result.get_points():    
            user_dict = {
            'time': point['time'],
            'sensor': point['sensor'],
            'state': point['state'],
            'value': point['value'],            
            }
            user_list.append(user_dict)
    
    


        return user_list, 200
