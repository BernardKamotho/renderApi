import os

# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pymysql
import pymysql.cursors

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)


# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Employee(Resource):
    
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        connection = pymysql.connect(host='localhost', user='root', password='', database='HyraxEmpDB')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "select * from employees"
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return jsonify({'message': 'No Records'})
        else:
            employees = cursor.fetchall()
            return jsonify(employees)
        #postgres://employees_u138_user:tbnE5fT3jMNnENCcHAc5y0DrpoeoIpAn@dpg-cho8qlpmbg50pip9mh20-a.oregon-postgres.render.com/employees_u138

    # Corresponds to POST request
    def post(self):
        data = request.json
        id_number = data['id_number']
        username = data['username']
        others = data['others']
        salary = data['salary']
        department = data['department']

        connection = pymysql.connect(host='localhost', user='root', password='', database='HyraxEmpDB')
        cursor = connection.cursor()
        sql = "insert into employees (id_number, username, others, salary, department) values(%s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (id_number, username, others, salary, department))
            connection.commit()
            return jsonify({'message': 'POST SUCCESS. RECORD SAVED'})
        except:
            connection.rollback()
            return jsonify({'message': 'POST FAILED. RECORD NOT SAVED'})

    # Delete a resource
    def delete(self):
        data = request.json
        id_number = data['id_number']
        connection = pymysql.connect(host='localhost', user='root', password='', database='HyraxEmpDB')
        cursor = connection.cursor()
        sql = "delete from employees where id_number = %s"
        try:
            cursor.execute(sql, (id_number))
            connection.commit()
            return jsonify({'message': 'DELETE SUCCESS'})
        except:
            connection.rollback()
            return jsonify({'message': 'DELETE FALILED'})

    # This updates a resource
    def put(self):
        data = request.json
        id_number = data['id_number']
        salary = data['salary']
        connection = pymysql.connect(host='localhost', user='root', password='', database='HyraxEmpDB')
        cursor = connection.cursor()
        sql = "update employees SET salary = %s where id_number  =%s"
        try:
            cursor.execute(sql, (salary, id_number))
            connection.commit()
            return jsonify({'message': 'UPDATE SUCCESS'})

        except:
            connection.rollback()
            return jsonify({'message': 'UPDATE FAILED'})


# adding the defined resources along with their corresponding urls
api.add_resource(Employee, '/employees')

# driver function
if __name__ == '__main__':
    app.run(debug=True)