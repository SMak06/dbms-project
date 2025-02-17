from flask.wrappers import Response
import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request, render_template, redirect, url_for, render_template_string
import random


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/admin')
def adminpage():
	return render_template('admin.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
				error = 'Invalid Credentials. Please try again.'
		else:
				return redirect(url_for('adminpage'))
	return render_template('adminlogin.html', error=error)


@app.route('/userlogin', methods=['GET', 'POST'])
def userloginpage():
	error = None
	if request.method == 'POST':
		_json = request.form.to_dict(flat=False)
		print(_json)
		try:
			_json = request.form.to_dict(flat=False)
			_email = _json['username']
			_password = _json['password']
			
			query = "SELECT p_id from smjl_customer where c_email = %s and password=%s"
			
			bData = (_email, _password)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(query, bData)
			rows = cursor.fetchall()
			conn.commit()
			
			if cursor.rowcount == 0:
				error = 'Invalid Credentials. Please try again.'
			else:
				return render_template('userdashboard.html', id = rows[0]['p_id'])
		except Exception as e:
			print(e)
			error = 'Server error. Please try again.'
		finally:
			cursor.close() 
			conn.close()
	return render_template('adminlogin.html', error=error)

@app.route('/user')
def userpage():
	return render_template('user.html')

# ADMIN

@app.route('/customers')
def get_all_customers():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from smjl_customer")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/airlines')
def getairlines():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from smjl_airlines")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/passengers')
def get_all_passengers():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from smjl_passenger")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/flights')
def get_all_flights():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from smjl_flight")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/toptwocustomers') 
def get_top_two_customers():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT p_id, count(smjl_customer_p_id) as numberOfBookings from smjl_customer, smjl_booking where p_id = smjl_customer_p_id group by p_id order by numberOfBookings desc limit 2")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/toptwoairlines') 
def get_top_two_airlines():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT al_name, count(f_id) from smjl_airlines, smjl_flight where al_id=smjl_airlines_al_id group by al_name order by count(f_id) desc limit 2;")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/toptwomemberships') 
def get_top_two_memberships():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT m_id, m_name, count(p_id) from smjl_club_memberships group by m_id order by count(p_id) desc limit 2;")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()
		

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

# USER

@app.route('/addcustomer', methods=['GET','POST'])
def add_cust():
	error = None
	if request.method == 'POST':
		try:
			_json = request.form.to_dict(flat=False)
			_nationality = _json['nationality']
			_email = _json['email']
			_phone = _json['phone']
			_passengers_alongside = _json['passengers_alongside']	
			_emergency_fname=_json['emergency_fname']
			_emergency_lname=_json['emergency_lname']	
			_emergency_phone=_json['emergency_phone']	
			_password = _json['password']
			_fname = _json['fname']
			_lname = _json['lname']
			_dob = _json['dob']
			_gender = _json['gender']
			_passport_number = _json['passport_number']
			_passport_expiry = _json['passport_expiry']

			if request.method == 'POST':	
				p_id = random.randint(1, 10000)		

				sqlQuery1 = "INSERT INTO smjl_passenger VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
				bindData1 = (p_id, _fname, _lname, _dob, _nationality, _gender, _passport_number, _passport_expiry)

				sqlQuery = "INSERT INTO smjl_customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
				bindData = (p_id, _email, _phone, _nationality, _passengers_alongside, _emergency_fname, _emergency_lname, _emergency_phone, _password)
			
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sqlQuery1, bindData1)
				cursor.execute(sqlQuery, bindData)
				conn.commit()

				respone = jsonify('Customer and Passenger added successfully!')
				respone.status_code = 200
				return respone
			else:
				return not_found()
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
	else:
		return render_template('signup.html', error=error)


@app.route('/bookings/<id>') 
def get_bookings(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		query = "SELECT * from smjl_booking where smjl_customer_p_id = %s"
		bData = (id)
		cursor.execute(query, bData)
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/insuranceplans/<id>') 
def get_insurance_plans(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		query = "select ip_id as InsuranceID, ip_name as InsuranceName from smjl_insurance_plans, smjl_ip_p, smjl_passenger where ip_id=smjl_insurance_plans_ip_id and smjl_passenger_p_id=p_id and p_id=%s"
		bData = (id)
		cursor.execute(query, bData)
		rows = cursor.fetchall()
		respone = jsonify(rows)
		print(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/flights/<id>')
def get_flights(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		query = "select b_id as BookingID, f_id as FlightID, f_arrival_airport, f_departure_airport from smjl_flight, smjl_b_f, smjl_booking, smjl_passenger where smjl_flight_f_id=f_id and smjl_booking_b_id=b_id and smjl_customer_p_id=smjl_booking_p_id and smjl_customer_p_id=p_id and p_id=%s"
		bData = (id)
		cursor.execute(query, bData)
		rows = cursor.fetchall()
		respone = jsonify(rows)
		print(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()


if __name__ == "__main__":
    app.run()


