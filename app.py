# app.py
from lib2to3.pytree import convert
from flask import Flask, flash, request, jsonify
from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd
from flask import Flask, flash, request, jsonify
from flaskext.mysql import MySQL


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


app = Flask(__name__)

mysql = MySQL()

if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

tunnel = SSHTunnelForwarder(('47.250.49.41', 22), ssh_password="123456Aa!", ssh_username="root",
                            remote_bind_address=("127.0.0.1", 3306))
tunnel.start()


conp = pymysql.connect(host='127.0.0.1', user="root",
                       passwd="123456Aa!", port=tunnel.local_bind_port)


mysql.init_app(app)


# employee table
@app.route('/create_employee', methods=['POST'])
def create_emp():
    try:

        _json = request.json
        _emp_id = _json['emp_id']
        _name = _json['emp_name']
        _surname = _json['emp_surname']
        _tel = _json['emp_tel']
        _village = _json['village']
        _district = _json['district']
        _pos_ID = _json['pos_ID']
        _dep_ID = _json['dep_ID']
        _provID = _json['prov_ID']
        _emp_profilepic = _json['emp_profilepic']
        if _emp_id and _name and _surname and _tel and _village and _district and _pos_ID and _dep_ID and _provID and _emp_profilepic:
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO test.employee(emp_id, emp_name, emp_surname, emp_tel, village, district, pos_ID, dep_ID, prov_ID, emp_profilepic) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            _emp_profilepic = convertToBinaryData(_emp_profilepic)
            bindData = (_emp_id, _name, _surname, _tel, _village,
                        _district, _pos_ID, _dep_ID, _provID, _emp_profilepic)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)


@app.route('/employee')
def emp():
    try:
        conn = conp
        # cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute("SELECT * FROM test.employee")
        # row = cursor.fetchall()
        # return jsonify(row)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT emp_name, emp_surname, emp_tel, village, district, pos_ID, dep_ID, prov_ID, emp_profilepic FROM test.employee")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)



@app.route('/employee/<string:emp_id>')
def emp_details(emp_id):
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT emp_name, emp_surname, emp_tel, village, district, pos_ID, dep_ID, prov_ID, emp_profilepic FROM test.employee WHERE id = %s", emp_id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.route('/update_employee', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _name = _json['emp_name']
        _surname = _json['emp_surname']
        _tel = _json['emp_tel']
        _village = _json['village']
        _district = _json['district']
        _pos_ID = _json['pos_ID']
        _dep_ID = _json['dep_ID']
        _provID = _json['prov_ID']
        _emp_profilepic = _json['emp_profilepic']
        if _name and _surname and _tel and _village and _district and _pos_ID and _dep_ID and _provID and _emp_profilepic and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE test.employee SET emp_name = %s, emp_surname = %s, emp_tel = %s, village = %s, district = %s, pos_ID = %s, dep_ID = %s, prov_ID = %s, emp_profilepic = %s WHERE id = %s"
            _emp_profilepic = convertToBinaryData(_emp_profilepic)
            bindData = (_name, _surname, _tel, _village, _district,
                        _pos_ID, _dep_ID, _provID, _emp_profilepic, _json['id'])
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)






@app.route('/delete_employee/<string:id>', methods=['DELETE'])
def delete_emp(id):
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test.employee WHERE id =%s", (id,))
        conn.commit()
        respone = jsonify('Employee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

# province_table


@app.route('/create_province', methods=['POST'])
def create_province():
    try:
        _json = request.json
        _province = _json['province']
        if _province and request.method == 'POST':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO test.province(province) VALUES(%s)"
            bindData = (_province)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Province added successfully!')
            respone.status_code = 200
    
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)






@app.route('/province', methods=['GET'])
def province():
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute("SELECT prov_ID, province FROM test.province")
        provRows = cursor.fetchall()
        respone = jsonify(provRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.route('/province/<int:prov_id>', methods=['GET'])
def province_details(prov_id):
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT prov_ID, province FROM test.province WHERE prov_ID = %s", prov_id)
        provRow = cursor.fetchone()
        respone = jsonify(provRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.route('/update_province', methods=['PUT'])
def update_province():
    try:
        _json = request.json
        _provID = _json['prov_ID']
        _province = _json['province']
        checkprovince = _province.isalpha()
        if _provID and checkprovince and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE test.province SET province = %s WHERE prov_ID = %s"
            bindData = (_province, _provID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Province updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)






@app.route('/delete_province/<int:prov_id>', methods=['DELETE'])
def delete_province(prov_id):
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM test.province WHERE prov_ID =%s", (prov_id,))
        conn.commit()
        respone = jsonify('Province deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)





# department_table


@app.route('/create_department', methods=['POST'])
def create_department():
    try:
        _json = request.json
        _dep_ID = _json['dep_ID']
        _dep_name = _json['dep_name']
        _dep_created_date = _json['dep_created_date']
        _dep_level = _json['dep_level']
        if _dep_ID and _dep_name and _dep_created_date and _dep_level and request.method == 'POST':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO test.department(dep_ID, dep_name, dep_created_date, dep_level) VALUES(%s, %s, %s, %s)"
            bindData = (_dep_ID, _dep_name, _dep_created_date, _dep_level)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Department added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)






@app.route('/department', methods=['GET'])
def department():
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT dep_ID, dep_name, dep_created_date, dep_level FROM test.department")
        depRows = cursor.fetchall()
        respone = jsonify(depRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.route('/department/<string:dep_id>', methods=['GET'])
def department_details(dep_id):
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT dep_ID, dep_name, dep_created_date, dep_level FROM test.department WHERE dep_ID = %s", dep_id)
        depRow = cursor.fetchone()
        respone = jsonify(depRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.route('/update_department', methods=['PUT'])
def update_department():
    try:
        _json = request.json
        _dep_ID = _json['dep_ID']
        _dep_name = _json['dep_name']
        _dep_created_date = _json['dep_created_date']
        _dep_level = _json['dep_level']
        if _dep_ID and _dep_name and _dep_created_date and _dep_level and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE test.department SET dep_name = %s, dep_created_date = %s, dep_level = %s WHERE dep_ID = %s"
            bindData = (_dep_name, _dep_created_date, _dep_level, _dep_ID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Department updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)






@app.route('/delete_department/<string:dep_id>', methods=['DELETE'])
def delete_department(dep_id):
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM test.department WHERE dep_ID =%s", (dep_id,))
        conn.commit()
        respone = jsonify('Department deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)





# position_table


@app.route('/create_position', methods=['POST'])
def create_position():
    try:
        _json = request.json
        _pos_ID = _json['pos_ID']
        _pos_name = _json['pos_name']
        if _pos_ID and _pos_name and request.method == 'POST':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO test.position(pos_ID, pos_name) VALUES(%s, %s)"
            bindData = (_pos_ID, _pos_name)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Position added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)






@app.route('/position', methods=['GET'])
def position():
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT pos_ID, pos_name FROM test.position")
        posRows = cursor.fetchall()
        respone = jsonify(posRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.route('/position/<string:pos_id>', methods=['GET'])
def position_details(pos_id):
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT pos_ID, pos_name FROM test.position WHERE pos_ID = %s", pos_id)
        posRow = cursor.fetchone()
        respone = jsonify(posRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)






@app.route('/update_position', methods=['PUT'])
def update_position():
    try:
        _json = request.json
        _pos_ID = _json['pos_ID']
        _pos_name = _json['pos_name']
        if _pos_ID and _pos_name and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE test.position SET pos_name = %s WHERE pos_ID = %s"
            bindData = (_pos_name, _pos_ID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Position updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)






@app.route('/delete_position/<string:pos_id>', methods=['DELETE'])
def delete_position(pos_id):
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test.position WHERE pos_ID =%s", (pos_id,))
        conn.commit()
        respone = jsonify('Position deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


#user_table
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        _json = request.json
        _emp_id = _json['emp_id']
        _password = _json['password']
        _user_type = _json['user_type']
        if _password and _user_type and _emp_id and request.method == 'POST':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO test.user(password, user_type, emp_id) VALUES(%s, %s, %s)"
            bindData = (_password, _user_type, _emp_id)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)


@app.route('/user', methods=['GET'])
def user():
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM test.user")
        userRows = cursor.fetchall()
        respone = jsonify(userRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

@app.route('/user/<string:user_id>', methods=['GET'])
def user_details(user_id):
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM test.user WHERE emp_id = %s", user_id)
        userRow = cursor.fetchone()
        respone = jsonify(userRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/update_user', methods=['PUT'])
def update_user():
    try:
        _json = request.json
        _emp_id = _json['emp_id']
        _password = _json['password']
        _user_type = _json['user_type']
        if _emp_id and _password and _user_type and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE test.user SET password = %s, user_type = %s WHERE emp_id = %s"
            bindData = (_password, _user_type, _emp_id)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)


@app.route('/delete_user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test.user WHERE emp_id =%s", (user_id,))
        conn.commit()
        respone = jsonify('User deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


