#!C:/Users/lx615/AppData/Local/Programs/Python/Python38-32/python

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import mysql.connector
import hashlib
import sys
import datetime
from dateutil.relativedelta import relativedelta

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
					   user='root',
					   password='',
					   database='flight_ticket')


#Define a route to hello function
@app.route('/')
def hello():
	if "identity" in session:
		session.pop("username")
		session.pop("identity")
	error = None
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE f.departure_time > \'{}\'\
			order by f.departure_time"
	cursor = conn.cursor()
	cursor.execute(query.format(now))
	data = cursor.fetchall()
	query = "select distinct airport_city from airport"
	cursor.execute(query)
	city = cursor.fetchall()
	city = [i[0] for i in city]
	query = "select distinct flight_num from flight"
	cursor.execute(query)
	flight = cursor.fetchall()
	flight = [int(i[0]) for i in flight]
	conn.commit()
	cursor.close()
	return render_template('index.html', data=data, error=error,city=city, flight=flight)

@app.route('/indexSearch', methods=['GET', 'POST'])
def indexSearch():

	if True:
		error=None
		if request.method == "POST":
			if "flight_num" in request.form:
				flight_num = request.form["flight_num"]
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.flight_num = \'{}\'"
				cursor = conn.cursor()
				cursor.execute(query.format(int(flight_num)))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				query = "select distinct flight_num from flight"
				cursor.execute(query)
				flight = cursor.fetchall()
				flight = [int(i[0]) for i in flight]
				conn.commit()
				cursor.close()
				return render_template('index.html', data=data, city=city,flight=flight)
			departure_city = request.form['departure_city']
			arrival_city = request.form['arrival_city']
			start_date = request.form['start_date']
			end_date = request.form['end_date']
			if departure_city == "None" and arrival_city == "None":
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				query = "select distinct flight_num from flight"
				cursor.execute(query)
				flight = cursor.fetchall()
				flight = [int(i[0]) for i in flight]
				conn.commit()
				cursor.close()
				return render_template('index.html', data=data, city=city,flight=flight)
			elif departure_city == "None":
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE a.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(departure_city, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				query = "select distinct flight_num from flight"
				cursor.execute(query)
				flight = cursor.fetchall()
				flight = [int(i[0]) for i in flight]
				conn.commit()
				cursor.close()
				return render_template('index.html', data=data, city=city,flight=flight)
			elif arrival_city == "None":
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE b.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(arrival_city, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				query = "select distinct flight_num from flight"
				cursor.execute(query)
				flight = cursor.fetchall()
				flight = [int(i[0]) for i in flight]
				conn.commit()
				cursor.close()
				return render_template('index.html', data=data, city=city,flight=flight)
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE a.airport_city = \'{}\' \
				and b.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
			cursor = conn.cursor()
			cursor.execute(query.format(departure_city, arrival_city, start_date, end_date))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			query = "select distinct flight_num from flight"
			cursor.execute(query)
			flight = cursor.fetchall()
			flight = [int(i[0]) for i in flight]
			conn.commit()
			cursor.close()
			return render_template('index.html', data=data, error=error, city=city,flight=flight)
		#cursor.close()
		#return render_template('search.html')


#Define route for login customer (default)
@app.route('/login_customer')
def login_customer():
	return render_template('login_customer.html')

#Define route for login agency
@app.route('/login_agency')
def login_agency():
	return render_template('login_agency.html')

#Define route for login staff
@app.route('/login_staff')
def login_staff():
	return render_template('login_staff.html')

#Define route for register
@app.route('/register_customer')
def register_customer():
	return render_template('register_customer.html')

@app.route('/register_agent')
def register_agent():
	return render_template('register_agent.html')

@app.route('/register_staff')
def register_staff():
	return render_template('register_staff.html')

#Authenticates the login
@app.route('/loginAuthCustomer', methods=['GET', 'POST'])
def loginAuthCustomer():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM customer WHERE email = \'{}\' and password = md5(\'{}\')"
	cursor.execute(query.format(email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		session['identity'] = "customer"
		return redirect(url_for('homeCustomer'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_customer.html', error=error)

#Authenticates the login
@app.route('/loginAuthAgency', methods=['GET', 'POST'])
def loginAuthAgency():
	#grabs information from the forms
	booking_agent_id = request.form['booking_agent_id']
	password = request.form['password']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM booking_agent WHERE booking_agent_id = \'{}\' and password = md5(\'{}\')"
	cursor.execute(query.format(booking_agent_id, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = booking_agent_id
		session['identity'] = "agent"
		return redirect(url_for('homeAgent'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_agency.html', error=error)

#Authenticates the login
@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM airline_staff WHERE username = \'{}\' and password = md5(\'{}\')"
	cursor.execute(query.format(username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['identity'] = "staff"
		return redirect(url_for('homeStaff'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_staff.html', error=error)

#Authenticates the register
@app.route('/registerAuth_customer', methods=['GET', 'POST'])
def registerAuth_customer():
	#grabs information from the forms
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']


#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM customer WHERE email= \'{}\'"
	cursor.execute(query.format(email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_customer.html', error = error)
	else:
		ins = "INSERT INTO customer VALUES(\'{}\', \'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		cursor.close()
		flash("You are logged in")
		return render_template('index.html')


@app.route('/registerAuth_agent', methods=['GET', 'POST'])    
def registerAuth_agent():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
	cursor.execute(query.format(email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_agent.html', error = error)
	else:
		ins = "INSERT INTO booking_agent VALUES(\'{}\', md5(\'{}\'), \'{}\')"
		cursor.execute(ins.format(email, password, booking_agent_id))
		conn.commit()
		cursor.close()
		flash("You are logged in")
		return render_template('index.html')


@app.route('/registerAuth_staff', methods=['GET', 'POST'])
def registerAuth_staff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']

#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
	cursor.execute(query.format(username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_staff.html', error = error)
	else:
		ins = "INSERT INTO airline_staff VALUES(\'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		flash("You are logged in")
		return render_template('index.html')

@app.route('/homeCustomer', methods=['GET', 'POST'])
def homeCustomer():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "You have logged out. Please log in again.")

	if identity == "customer":
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE p.customer_email = \'{}\' \
				and f.departure_time > \'{}\' \
				order by f.departure_time"
		print(now, file=sys.stdout)
		cursor = conn.cursor()
		cursor.execute(query.format(username, now))
		data = cursor.fetchall()

		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		print(city, file=sys.stdout)
		conn.commit()
		cursor.close()
		return render_template('homeCustomer.html', username=username, data=data, city=city)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")

@app.route('/myflightCustomer', methods=['GET', 'POST'])
def myflightCustomer():

	username = session['username']
	
	if request.method == "POST":
		departure_city = request.form['departure_city']
		arrival_city = request.form['arrival_city']
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		if departure_city == "None" and arrival_city == "None":
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE p.customer_email = \'{}\' \
			and f.departure_time >= \'{}\'\
			and f.departure_time <= \'{}\'\
			order by f.departure_time"
			cursor = conn.cursor()
			cursor.execute(query.format(username, start_date, end_date))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			conn.commit()
			cursor.close()
			return render_template('homeCustomer.html', data=data, username=username, city=city)
		elif departure_city == "None":
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE p.customer_email = \'{}\' \
			and a.airport_city = \'{}\' \
			and f.departure_time >= \'{}\'\
			and f.departure_time <= \'{}\'\
			order by f.departure_time"
			cursor = conn.cursor()
			cursor.execute(query.format(username, departure_city, start_date, end_date))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			conn.commit()
			cursor.close()
			return render_template('homeCustomer.html', data=data, username=username, city=city)
		elif arrival_city == "None":
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE p.customer_email = \'{}\' \
			and b.airport_city = \'{}\' \
			and f.departure_time >= \'{}\'\
			and f.departure_time <= \'{}\'\
			order by f.departure_time"
			cursor = conn.cursor()
			cursor.execute(query.format(username, arrival_city, start_date, end_date))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			conn.commit()
			cursor.close()
			return render_template('homeCustomer.html', data=data, username=username, city=city)
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE p.customer_email = \'{}\' \
			and a.airport_city = \'{}\' \
			and b.airport_city = \'{}\' \
			and f.departure_time >= \'{}\'\
			and f.departure_time <= \'{}\'\
			order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(username, departure_city, arrival_city, start_date, end_date))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
	return render_template('homeCustomer.html', data=data, username=username, city=city)
	#cursor.close()
	#return render_template('search.html')

@app.route('/buyCustomer', methods=['GET', 'POST'])
def buyCustomer():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "You have logged out. Please log in again.")

	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if identity == "customer":
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('buyCustomer.html', data=data, username=username, message="Succssfully bought", city=city, flight=data)
	else:	
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")

@app.route('/buyflightCustomer', methods=['GET', 'POST'])
def buyflightCustomer():

	username = session['username']
	
	if request.method == "POST":
		cursor = conn.cursor()
		row = request.form['button']
		print(row, file=sys.stdout)
		flight_num = int(row.split(",")[1].strip())
		airplne_id = int(row.split(",")[-1][:-1].strip())
		query = "select count(distinct t.ticket_id) from purchases p join ticket t using (ticket_id) where flight_num=\'{}\'"
		cursor.execute(query.format(flight_num))
		bought = cursor.fetchone()
		bought = int(bought[0])
		query = "select seats from airplane a where a.airplane_id = \'{}\'"
		cursor.execute(query.format(airplne_id))
		seats = cursor.fetchone()
		seats = int(seats[0])
		print("seats", seats, bought, file=sys.stdout)
		if seats <= bought:
			print("seats", seats, bought, file=sys.stdout)
			row = request.form['button']
			flight_num = int(row.split(",")[1].strip())
			print(type(row), file=sys.stdout)
			now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
			cursor = conn.cursor()
			cursor.execute(query.format(now))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
			cursor.execute(query.format(now))
			flight = cursor.fetchall()
			conn.commit()
			cursor.close()
			return render_template('buyCustomer.html', data=data, username=username, message="Succssfully bought", error = "Seats sold out.", flight_num = flight_num, city=city, flight=flight)
		
		query = "select max(ticket_id) from ticket"
		cursor.execute(query)
		new_ticket_id = int(cursor.fetchone()[0])+1
		query2 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
		row = request.form['button']
		flight_num = int(row.split(",")[1].strip())
		airline_name = row.split(",")[0].split("(")[1].strip(""" '" """)
		purchase_date = datetime.date.today().strftime("%Y-%m-%d")
		print(type(new_ticket_id), file=sys.stdout)
		print(type(flight_num), file=sys.stdout)
		cursor.execute(query2.format(new_ticket_id, airline_name, flight_num))
		query3 = "INSERT INTO purchases (ticket_id, customer_email, purchase_date) VALUES (\'{}\', \'{}\', \'{}\')"
		cursor.execute(query3.format(new_ticket_id, username, purchase_date))
		conn.commit()
		cursor.close()
		#print(type(button), file=sys.stdout)
		return redirect(url_for('homeCustomer'))

@app.route('/searchflightCustomer', methods=['GET', 'POST'])
def searchflightCustomer():

	username = session['username']
	
	if request.method == "POST":
		# departure_city_temp = "(select a.airport_city from airport a join flight f on f.departure_airport= a.airport_name)"
		# arrival_city_temp = "(select a.airport_city from airport a join flight f on f.arrival_airport= a.airport_name)"
		# start_date_temp = "(select min(f.departure_time) from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE f.status='upcoming')"
		# end_date_temp = "(select max(f.departure_time) from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE f.status='upcoming')"
		departure_city = request.form['departure_city']
		arrival_city = request.form['arrival_city']
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		# print(departure_city, file=sys.stdout)
		# print(arrival_city, file=sys.stdout)
		# print(start_date, file=sys.stdout)
		# print(end_date, file=sys.stdout)
		# if departure_city == "None":
		# 	departure_city = departure_city_temp
		# else:
		# 	departure_city = "("+departure_city+")"
		# if arrival_city == "None":
		# 	arrival_city = arrival_city_temp
		# else:
		# 	arrival_city = "("+arrival_city+")"
		# if start_date == "None":
		# 	start_date = start_date_temp
		# if end_date == "None":
		# 	end_date = end_date_temp
		# print(departure_city, file=sys.stdout)
		# print(arrival_city, file=sys.stdout)
		# print(start_date, file=sys.stdout)
		# print(end_date, file=sys.stdout)

		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE a.airport_city = \'{}\' \
			and b.airport_city = \'{}\' \
			and f.departure_time >= \'{}\'\
			and f.departure_time <= \'{}\'\
			order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(departure_city, arrival_city, start_date, end_date))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		flight = cursor.fetchall()
		conn.commit()
		cursor.close()
	return render_template('buyCustomer.html', data=data, username=username, message="Succssfully bought", city=city, flight=flight)
	#cursor.close()
	#return render_template('search.html')

@app.route('/myspendingCustomer', methods=['GET', 'POST'])
def myspendingCustomer():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "You have logged out. Please log in again.")
	if identity == "customer":
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		before_day1 = (datetime.datetime.now()).strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=5)).strftime("%Y-%m-%d")
		query2 = "select year(g.purchase_date), month(g.purchase_date), sum(g.price) from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\' and p.booking_agent_id IS NULL) g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'\
				group by year(g.purchase_date), month(g.purchase_date)\
				order by year(g.purchase_date) desc, month(g.purchase_date) desc"
		query3 = "select year(g.purchase_date), month(g.purchase_date), sum(g.price)*1.1 from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\' and p.booking_agent_id IS NOT NULL) g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'\
				group by year(g.purchase_date), month(g.purchase_date)\
				order by year(g.purchase_date) desc, month(g.purchase_date) desc"
		cursor.execute(query2.format(username, before_day2, before_day1))
		spending_graph = cursor.fetchall()
		cursor.execute(query3.format(username, before_day2, before_day1))
		spending_graph2 = cursor.fetchall()
		print("sg", spending_graph, spending_graph2, file=sys.stdout)
		#print(spending_graph, file=sys.stdout)
		x_date = [(datetime.datetime.strptime(before_day2,"%Y-%m-%d")+relativedelta(months=i)).strftime("%Y-%m") for i in range(6)]
		print("x_date",x_date, file=sys.stdout)
		spending_date = [datetime.date(int(i[0]), int(i[1]), 1).strftime("%Y-%m") for i in spending_graph] + [datetime.date(int(i[0]), int(i[1]), 1).strftime("%Y-%m") for i in spending_graph2]
		spending_s = [i[2] for i in spending_graph] + [i[2] for i in spending_graph2]
		y_spending = []
		for i in x_date:
			if i in spending_date:
				temp = 0
				for j in range(len(spending_date)):
					if i == spending_date[j]:
						temp += spending_s[j]
				y_spending.append(temp)
			else:
				y_spending.append(0)
		#y_spending = [spending_s[spending_date.index(i)] if i in spending_date else 0 for i in x_date]
		print(spending_date, file=sys.stdout)
		#print(x_date, file=sys.stdout)
		#print(y_spending, file=sys.stdout)
		conn.commit()
		cursor.close()
		if request.method == "POST":
			before_day1 = request.form['end_date']
			before_day2 = request.form["start_date"]
			start_date = datetime.datetime.strptime(before_day2,"%Y-%m")
			end_date = datetime.datetime.strptime(before_day1,"%Y-%m")
			cursor = conn.cursor()
			query2 = "select year(g.purchase_date), month(g.purchase_date), sum(g.price) from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\' and p.booking_agent_id IS NULL) g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'\
				group by year(g.purchase_date), month(g.purchase_date)\
				order by year(g.purchase_date) desc, month(g.purchase_date) desc"
			query3 = "select year(g.purchase_date), month(g.purchase_date), sum(g.price)*1.1 from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\' and p.booking_agent_id IS NOT NULL) g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'\
				group by year(g.purchase_date), month(g.purchase_date)\
				order by year(g.purchase_date) desc, month(g.purchase_date) desc"
			cursor.execute(query2.format(username, start_date.strftime("%Y-%m-%d"), (end_date+relativedelta(months=1)).strftime("%Y-%m-%d")))
			spending_graph = cursor.fetchall()
			months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
			cursor.execute(query3.format(username, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
			spending_graph2 = cursor.fetchall()
			print(before_day2, before_day1, months, file=sys.stdout)
			#print(spending_graph, file=sys.stdout)
			x_date = [(start_date+relativedelta(months=i)).strftime("%Y-%m") for i in range(months+1)]
			spending_date = [datetime.date(int(i[0]), int(i[1]), 1).strftime("%Y-%m") for i in spending_graph]+[datetime.date(int(i[0]), int(i[1]), 1).strftime("%Y-%m") for i in spending_graph2]
			print(spending_date, file=sys.stdout)
			spending_s = [i[2] for i in spending_graph]+[i[2] for i in spending_graph2]
			y_spending = []
			for i in x_date:
				if i in spending_date:
					temp = 0
					for j in range(len(spending_date)):
						if i == spending_date[j]:
							temp += spending_s[j]
					y_spending.append(temp)
				else:
					y_spending.append(0)
			#print(x_date, file=sys.stdout)
			#print(y_spending, file=sys.stdout)
			conn.commit()
			cursor.close()
			return render_template('MySpendingCustomer.html', username = username, total=int(float(sum(y_spending))), labels=x_date, values=y_spending, title1 = "Total Spending From "+str(x_date[0])+" to "+str(x_date[-1])+":",title2 = "My Spending From "+str(x_date[0])+" to "+str(x_date[-1]), max_val = int(float(max(y_spending))+300))
		return render_template('MySpendingCustomer.html', username = username, total=int(float(sum(y_spending))), labels=x_date, values=y_spending, title1 = "Total Spending in the Past Year:", title2 = "My Spending in the Past Six Months", max_val = int(float(max(y_spending))+300))
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")








#Agent
@app.route('/homeAgent')
def homeAgent():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "You have logged out. Please log in again.")
	if identity == "agent":
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE p.booking_agent_id = \'{}\' \
				and f.departure_time>\'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(username, now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('homeAgent.html', username=username, data=data, city=city)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")

@app.route('/myflightAgent', methods=['GET', 'POST'])
def myflightAgent():

	username = session['username']
	identity = session['identity']
	
	if identity == "agent":
		if request.method == "POST":
			departure_city = request.form['departure_city']
			arrival_city = request.form['arrival_city']
			start_date = request.form['start_date']
			end_date = request.form['end_date']
			if departure_city == "None" and arrival_city == "None":
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE p.booking_agent_id = \'{}\'\
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(username, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				conn.commit()
				cursor.close()
				return render_template('homeAgent.html', data=data, username=username, city=city)
			elif departure_city == "None":
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE p.booking_agent_id = \'{}\'\
				and a.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(username, departure_city, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				conn.commit()
				cursor.close()
				return render_template('homeAgent.html', data=data, username=username, city=city)
			elif arrival_city == "None":
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE p.booking_agent_id = \'{}\'\
				and b.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(username, arrival_city, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				conn.commit()
				cursor.close()
				return render_template('homeAgent.html', data=data, username=username, city=city)
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE p.booking_agent_id = \'{}\'\
				and a.airport_city = \'{}\' \
				and b.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
			cursor = conn.cursor()
			cursor.execute(query.format(username, departure_city, arrival_city, start_date, end_date))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			conn.commit()
			cursor.close()
		return render_template('homeAgent.html', data=data, username=username, city=city)
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		cursor.execute(query)
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")

@app.route('/buyAgent', methods=['GET', 'POST'])
def buyAgent():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "You have logged out. Please log in again.")
	
	error = None
	if identity == "agent":
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor.execute(query.format(now))
		flight = cursor.fetchall()
		conn.commit()
		cursor.close()
		return render_template('buyAgent.html', data=data, username=username, message="Succssfully bought", error = error, city=city, flight=flight)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")

@app.route('/buyflightAgent', methods=['GET', 'POST'])
def buyflightAgent():

	username = session['username']
	
	if request.method == "POST":
		print(request.form, file=sys.stdout)
		customer_email = request.form["customer_email"]
		cursor = conn.cursor()
		query = "select email from customer where email=\'{}\'"
		cursor.execute(query.format(customer_email))
		email_list = cursor.fetchone()
		row = request.form['button']
		print(row, file=sys.stdout)
		flight_num = int(row.split(",")[1].strip())
		airplne_id = int(row.split(",")[-1][:-1].strip())
		query = "select count(distinct t.ticket_id) from purchases p join ticket t using (ticket_id) where flight_num=\'{}\'"
		cursor.execute(query.format(flight_num))
		bought = cursor.fetchone()
		bought = int(bought[0])
		query = "select seats from airplane a where a.airplane_id = \'{}\'"
		cursor.execute(query.format(airplne_id))
		seats = cursor.fetchone()
		seats = int(seats[0])
		print("seats", seats, bought, file=sys.stdout)
		if seats <= bought:
			print("seats", seats, bought, file=sys.stdout)
			row = request.form['button']
			flight_num = int(row.split(",")[1].strip())
			print(type(row), file=sys.stdout)
			now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE f.departure_time > \'{}\'\
			order by f.departure_time"
			cursor.execute(query.format(now))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
			cursor.execute(query.format(now))
			flight = cursor.fetchall()
			conn.commit()
			cursor.close()
			return render_template('buyAgent.html', data=data, username=username, message="Succssfully bought", error = "Seats sold out.", flight_num = flight_num, city=city, flight=flight)

		if email_list is None:
			row = request.form['button']
			flight_num = int(row.split(",")[1].strip())
			print(type(row), file=sys.stdout)
			now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE f.departure_time > \'{}\'\
			order by f.departure_time"
			cursor.execute(query.format(now))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
			cursor.execute(query.format(now))
			flight = cursor.fetchall()
			conn.commit()
			cursor.close()
			return render_template('buyAgent.html', data=data, username=username, message="Succssfully bought", error = "Invalid Customer Email.", flight_num = flight_num, city=city, flight=flight)

		query = "select max(ticket_id) from ticket"
		cursor.execute(query)
		new_ticket_id = int(cursor.fetchone()[0])+1
		query2 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
		row = request.form['button']
		flight_num = int(row.split(",")[1].strip())
		airline_name = row.split(",")[0].split("(")[1].strip(""" '" """)
		purchase_date = datetime.date.today().strftime("%Y-%m-%d")
		print(type(new_ticket_id), file=sys.stdout)
		print(type(flight_num), file=sys.stdout)
		cursor.execute(query2.format(new_ticket_id, airline_name, flight_num))
		query3 = "INSERT INTO purchases VALUES (\'{}\',\'{}\', \'{}\', \'{}\')"
		cursor.execute(query3.format(new_ticket_id, customer_email, username, purchase_date))
		conn.commit()
		cursor.close()
		#print(type(button), file=sys.stdout)
		return redirect(url_for('homeAgent'))

@app.route('/searchflightAgent', methods=['GET', 'POST'])
def searchflightAgent():

	username = session['username']
	error = None
	
	if request.method == "POST":
		# departure_city_temp = "(select a.airport_city from airport a join flight f on f.departure_airport= a.airport_name)"
		# arrival_city_temp = "(select a.airport_city from airport a join flight f on f.arrival_airport= a.airport_name)"
		# start_date_temp = "(select min(f.departure_time) from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE f.status='upcoming')"
		# end_date_temp = "(select max(f.departure_time) from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE f.status='upcoming')"
		departure_city = request.form['departure_city']
		arrival_city = request.form['arrival_city']
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		# print(departure_city, file=sys.stdout)
		# print(arrival_city, file=sys.stdout)
		# print(start_date, file=sys.stdout)
		# print(end_date, file=sys.stdout)
		# if departure_city == "None":
		# 	departure_city = departure_city_temp
		# else:
		# 	departure_city = "("+departure_city+")"
		# if arrival_city == "None":
		# 	arrival_city = arrival_city_temp
		# else:
		# 	arrival_city = "("+arrival_city+")"
		# if start_date == "None":
		# 	start_date = start_date_temp
		# if end_date == "None":
		# 	end_date = end_date_temp
		# print(departure_city, file=sys.stdout)
		# print(arrival_city, file=sys.stdout)
		# print(start_date, file=sys.stdout)
		# print(end_date, file=sys.stdout)

		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE a.airport_city = \'{}\' \
			and b.airport_city = \'{}\' \
			and f.departure_time >= \'{}\'\
			and f.departure_time <= \'{}\'\
			order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(departure_city, arrival_city, start_date, end_date))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor.execute(query.format(now))
		flight = cursor.fetchall()
		conn.commit()
		cursor.close()
	return render_template('buyAgent.html', data=data, username=username, message="Succssfully bought", error=error, city=city, flight=flight)
	#cursor.close()
	#return render_template('search.html')

@app.route('/MyCommisionAgent', methods=['GET', 'POST'])
def MyCommisionAgent():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "You have logged out. Please log in again.")

	if identity == "agent":
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=1)).strftime("%Y-%m-%d")
		query2 = "select sum(g.price), count(g.ticket_id) from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.booking_agent_id = \'{}\') g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'"
		cursor.execute(query2.format(username, before_day2, before_day1))
		data = cursor.fetchone()
		if data[0]:
			total_commision = format(int(data[0])/10, ".2f")
			ticket_num = int(data[1])
			avg_commision = format(int(data[0])/10/ticket_num, ".2f")
		else:
			total_commision = 0
			ticket_num = 0
			avg_commision = 0
		conn.commit()
		cursor.close()
		if request.method == "POST":
			before_day1 = request.form['end_date']
			before_day2 = request.form["start_date"]
			cursor = conn.cursor()
			query2 = "select sum(g.price), count(g.ticket_id) from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.booking_agent_id = \'{}\') g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'"
			cursor.execute(query2.format(username, before_day2, before_day1))
			data = cursor.fetchone()
			if data[0]:
				total_commision = format(int(data[0])/10, ".2f")
				ticket_num = int(data[1])
				avg_commision = format(int(data[0])/10/ticket_num, ".2f")
			else:
				total_commision = 0
				ticket_num = 0
				avg_commision = 0
			conn.commit()
			cursor.close()
			return render_template('MyCommisionAgent.html', username = username, total=total_commision, ticket = ticket_num, avg = avg_commision, title1 = "Total Commision Fees From "+before_day2+" to "+before_day1+":",title2 = "Number of Tickets Sold From "+before_day2+" to "+before_day1+":", title3 = "Average Sold Ticket Price From "+before_day2+" to "+before_day1+":")
		return render_template('MyCommisionAgent.html', username = username, total=total_commision, ticket = ticket_num, avg = avg_commision, title1 = "Total Commision Fees in Past 30 Days:",title2 = "Number of Tickets Sold in Past 30 Days:", title3 = "Average Sold Ticket Price in Past 30 Days:")
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")

@app.route('/topcustomerAgent', methods=['GET', 'POST'])
def topcustomerAgent():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "You have logged out. Please log in again.")

	if identity == "agent":
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=6)).strftime("%Y-%m-%d")
		query2 = "select g.customer_email, sum(g.price)/10 total_commision from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date, p.customer_email \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.booking_agent_id = \'{}\') g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'\
				group by g.customer_email\
				order by sum(g.price) desc\
				limit 5"
		cursor.execute(query2.format(username, before_day2, before_day1))
		data = cursor.fetchall()
		x1 = [i[0] for i in data]
		y1 = [int(i[1]) for i in data]
		print(before_day2, before_day1, file=sys.stdout)
		print(data, file=sys.stdout)
		print(x1, y1, file=sys.stdout)
		query = "select g.customer_email, count(g.ticket_id) total_commision from \
				(SELECT distinct t.ticket_id, f.flight_num, f.price, p.purchase_date, p.customer_email \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id) WHERE p.booking_agent_id = \'{}\') g \
				where g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'\
				group by g.customer_email\
				order by count(g.ticket_id) desc\
				limit 5"
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=12)).strftime("%Y-%m-%d")
		cursor.execute(query.format(username, before_day2, before_day1))
		data = cursor.fetchall()
		#print(spending_graph, file=sys.stdout)
		x2 = [i[0] for i in data]
		y2 = [int(i[1]) for i in data]
		print(before_day2, before_day1, file=sys.stdout)
		print(data, file=sys.stdout)
		print(x2, y2, file=sys.stdout)
		if len(y1) != 0:
			max_val1 = int(float(max(y1))+100)
			max_val2 = int(float(max(y2))+1)
		else:
			max_val1 = 0
			max_val2 = 0
		conn.commit()
		cursor.close()
		return render_template('TopCustomerAgent.html', username = username, x1=x1, x2=x2, y1=y1, y2=y2, title1 = "Top 5 Customers in Total Commission Fees in Past Six Months", title2 = "Top 5 Customers in Number of Tickets Bought in the Past Year", max_val1 = max_val1, max_val2 = max_val2)
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, error = "Invalid Identity. Please return.")


#Staff
@app.route('/homeStaff', methods = ['GET', 'POST'])
def homeStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, city = city, error="You have logged out. Please log in again.")
	if identity == "staff":
		cursor = conn.cursor()
		test = "select airline_name from airline_staff where username = \'{}\'"
		cursor.execute(test.format(username))
		airline_name = cursor.fetchone()
		airline_name = airline_name[0]
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now() + relativedelta(months=1)).strftime("%Y-%m-%d")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.airline_name = \'{}\' and f.departure_time >= \'{}\' and f.departure_time <= \'{}\'\
				order by f.departure_time"
		cursor.execute(query.format(airline_name, before_day1, before_day2))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('homeStaff.html', username=username, city=city, data=data, data2=None)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, city = city, error="Invalid Identity. Please return.")

@app.route('/customerStaff', methods=['GET', 'POST'])
def customerStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', data=data, city=city, error="You have logged out. Please log in again.")
	if identity == "staff":
		username = session['username']
		if request.method == "POST":
			username = session['username']
			flight_num = request.form['flight_num']
			cursor = conn.cursor()
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			airline_name = cursor.fetchone()
			airline_name = airline_name[0]
			query = "Select distinct c.name, c.email from purchases p join ticket t using (ticket_id) join flight f using (flight_num) join customer c on c.email = p.customer_email\
					where f.flight_num = \'{}\' and f.airline_name = \'{}\'"
			cursor.execute(query.format(flight_num, airline_name))
			data = cursor.fetchall()
			conn.commit()
			cursor.close()
			return render_template('customerStaff.html', username =username, data = data)
		return render_template('customerStaff.html', username =username, data=None)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")

#Staff function below:
@app.route('/myflightStaff', methods=['GET', 'POST'])
def myflightStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']

		if request.method == "POST":
			departure_city = request.form['departure_city']
			arrival_city = request.form['arrival_city']
			start_date = request.form['start_date']
			end_date = request.form['end_date']
			if departure_city == "None" and arrival_city == "None":
				cursor = conn.cursor()
				test = "select airline_name from airline_staff where username = \'{}\'"
				cursor.execute(test.format(username))
				airline_name = cursor.fetchone()
				airline_name = airline_name[0]
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.airline_name = \'{}\' and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor.execute(query.format(airline_name, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				conn.commit()
				cursor.close()
				return render_template('homeStaff.html', city=city, data=data, username=username,data2=None)
			elif departure_city == "None":
				cursor = conn.cursor()
				test = "select airline_name from airline_staff where username = \'{}\'"
				cursor.execute(test.format(username))
				airline_name = cursor.fetchone()
				airline_name = airline_name[0]
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.airline_name = \'{}\' and a.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(airline_name, departure_city, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				conn.commit()
				cursor.close()
				return render_template('homeStaff.html', city=city, data=data, username=username,data2=None)
			elif arrival_city == "None":
				cursor = conn.cursor()
				test = "select airline_name from airline_staff where username = \'{}\'"
				cursor.execute(test.format(username))
				airline_name = cursor.fetchone()
				airline_name = airline_name[0]
				query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.airline_name = \'{}\' and b.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				order by f.departure_time"
				cursor = conn.cursor()
				cursor.execute(query.format(airline_name, arrival_city, start_date, end_date))
				data = cursor.fetchall()
				query = "select distinct airport_city from airport"
				cursor.execute(query)
				city = cursor.fetchall()
				city = [i[0] for i in city]
				conn.commit()
				cursor.close()
				return render_template('homeStaff.html', city=city, data=data, username=username, error=None, message=None, data2=None)
			cursor = conn.cursor()
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			airline_name = cursor.fetchone()
			airline_name = airline_name[0]
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.airline_name = \'{}\' and a.airport_city = \'{}\' \
				and b.airport_city = \'{}\' \
				and f.departure_time >= \'{}\'\
				and f.departure_time <= \'{}\'\
				and f.status='upcoming'\
				order by f.departure_time"
			cursor = conn.cursor()
			cursor.execute(query.format(airline_name, departure_city, arrival_city, start_date, end_date))
			data = cursor.fetchall()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			conn.commit()
			cursor.close()
		return render_template('homeStaff.html', city=city, data=data,data2=None, username=username, message=None, error=None, flight_num=None, departure_city = departure_city, arrival_city = arrival_city, start_date = start_date, end_date=end_date)
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")



##needs further work
@app.route('/statusStaff', methods=['GET', 'POST'])
def statusStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']

		if request.method == "POST":
			#print(request.form, file=sys.stdout)
			#flight_num = request.form["flight_num"]
			#airline_name = request.form["airline_name"]
			error = None
			cursor = conn.cursor()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			row = request.form['button']
			#data = request.form['data']
			#print(data, file=sys.stdout)
			flight_num = row.split(",")[1].strip()
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			airline_name = cursor.fetchone()
			airline_name = airline_name[0]
			status = request.form['status']
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			airline_name = cursor.fetchone()
			airline_name = airline_name[0]
			row = request.form['button']
			#data = request.form['data']
			#print(data, file=sys.stdout)
			flight_num = row.split(",")[1].strip()
			before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
			before_day2 = (datetime.datetime.now() + relativedelta(months=1)).strftime("%Y-%m-%d")
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE f.airline_name = \'{}\' and f.departure_time >= \'{}\' and f.departure_time <= \'{}\'\
			order by f.departure_time"
			cursor.execute(query.format(airline_name, before_day1, before_day2))
			data = cursor.fetchall()
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE f.airline_name = \'{}\' and f.flight_num = \'{}\'"
			cursor.execute(query.format(airline_name, int(flight_num)))
			data2 = cursor.fetchall()
			if status not in ["upcoming", "delayed", "in-progress"]:
				print("1", file=sys.stdout)
				return render_template('homeStaff.html', city=city, data=data, data2=data2, username=username, message=None, error = "Invalid Status Input.", flight_num = flight_num, flight=data2)
			query = "update flight set status = \'{}\' where airline_name = \'{}\' and flight_num = \'{}\'"
			cursor.execute(query.format(status, airline_name, int(flight_num)))
			print(status, airline_name, flight_num, type(int(flight_num)), file=sys.stdout)
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			airline_name = cursor.fetchone()
			airline_name = airline_name[0]
			row = request.form['button']
			#data = request.form['data']
			#print(data, file=sys.stdout)
			flight_num = row.split(",")[1].strip()
			before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
			before_day2 = (datetime.datetime.now() + relativedelta(months=1)).strftime("%Y-%m-%d")
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE f.airline_name = \'{}\' and f.departure_time >= \'{}\' and f.departure_time <= \'{}\'\
			order by f.departure_time"
			cursor.execute(query.format(airline_name, before_day1, before_day2))
			data = cursor.fetchall()
			query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
			from flight f join airline_staff s using (airline_name) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
			WHERE f.airline_name = \'{}\' and f.flight_num = \'{}\'"
			cursor.execute(query.format(airline_name, int(flight_num)))
			data2 = cursor.fetchall()
			print(data2, file=sys.stdout)
			conn.commit()
			cursor.close()
			return render_template('homeStaff.html', city=city, data=data, data2=data2, username=username, message="Flight status successfully updated.", error = error, flight_num = flight_num, flight=data2)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")



@app.route('/createflightStaff', methods=['GET', 'POST'])
def createflightStaff():
	#grabs information from the forms
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":
		username = session['username']
		if request.method == "POST":
			airline_name = request.form['airline_name']
			flight_num = request.form['flight_num']
			departure_airport = request.form['departure_airport']
			departure_time = request.form['departure_time']
			arrival_airport = request.form['arrival_airport']
			arrival_time = request.form['arrival_time']
			price = request.form['price']
			status = request.form['status']
			airplane_id = request.form['airplane_id']

			#cursor used to send queries
			cursor = conn.cursor()
			#executes query
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			test_data = cursor.fetchone()
			test_data = test_data[0]
			if airline_name == test_data:
				query = "SELECT * FROM flight WHERE airline_name = \'{}\' and flight_num = \'{}\'"
				cursor.execute(query.format(airline_name, int(flight_num)))
				#stores the results in a variable
				data = cursor.fetchone()
				#use fetchall() if you are expecting more than 1 data row
				error = None
				if(data):
					#If the previous query returns data, then user exists
					error = "This flight already exists"
					return render_template('createflightStaff.html', error = error, username=username)
				else:
					ins = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
					cursor.execute(ins.format(airline_name, int(flight_num), departure_airport, departure_time, arrival_airport, arrival_time, float(price), status, int(airplane_id)))
					conn.commit()
					cursor.close()
					#flash("You are logged in")
					return redirect(url_for('homeStaff'))
			return render_template('createflightStaff.html', error = "This flight doesn't belong to your airline", username=username)
		return render_template('createflightStaff.html', error = None, username=username)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")




@app.route('/addairplaneStaff', methods=['GET', 'POST'])
def addairplaneStaff():
	#grabs information from the forms
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":
		username = session['username']
		if request.method == "POST":
			airline_name = request.form['airline_name']
			airplane_id = request.form['airplane_id']
			seats = request.form['seats']

		#	if not len(password) >= 4:
		#                flash("Password length must be at least 4 characters")
		#               return redirect(request.url)

			#cursor used to send queries
			cursor = conn.cursor()
			#executes query
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			test_data = cursor.fetchone()
			test_data = test_data[0]
			if airline_name == test_data:
				query = "SELECT * FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
				cursor.execute(query.format(airline_name, airplane_id))
				#stores the results in a variable
				data = cursor.fetchone()
				#use fetchall() if you are expecting more than 1 data row
				error = None
				if(data):
					#If the previous query returns data, then user exists
					error = "This airplane already exists"
					return render_template('addairplaneStaff.html', error = error, username=username)
				else:
					ins = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"
					cursor.execute(ins.format(airline_name, airplane_id, seats))
					conn.commit()
					cursor.close()
					#flash("You are logged in")
					return redirect(url_for('homeStaff'))
			return render_template('addairplaneStaff.html', error = "This airplane doesn't belong to your airline.", username=username)
		return render_template('addairplaneStaff.html', error = None, username=username)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")




@app.route('/addairportStaff', methods=['GET', 'POST'])
def addairportStaff():
	#grabs information from the forms
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":
		if request.method == "POST":
			airport_name = request.form['airport_name']
			airport_city = request.form['airport_city']

		#	if not len(password) >= 4:
		#                flash("Password length must be at least 4 characters")
		#               return redirect(request.url)

			#cursor used to send queries
			cursor = conn.cursor()
			query = "select distinct airport_city from airport"
			cursor.execute(query)
			city = cursor.fetchall()
			city = [i[0] for i in city]
			#executes query
			query = "SELECT * FROM airport WHERE airport_name = \'{}\'"
			cursor.execute(query.format(airport_name))
			#stores the results in a variable
			data = cursor.fetchone()
			#use fetchall() if you are expecting more than 1 data row
			error = None
			if(data):
				#If the previous query returns data, then user exists
				error = "This airport already exists"
				return render_template('addairportStaff.html', city=city, error = error, username=username)
			else:
				ins = "INSERT INTO airport VALUES(\'{}\', \'{}\')"
				cursor.execute(ins.format(airport_name, airport_city))
				conn.commit()
				cursor.close()
				#flash("You are logged in")
				return redirect(url_for('homeStaff'))
		cursor = conn.cursor()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('addairportStaff.html', city=city, error = None, username=username)
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")



@app.route('/viewagentsStaff', methods=['GET', 'POST'])
def viewagentsStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		test = "select airline_name from airline_staff where username = \'{}\'"
		cursor.execute(test.format(username))
		airline_name = cursor.fetchone()
		airline_name = airline_name[0]
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=1)).strftime("%Y-%m-%d")
		query2 = "Select p.customer_email, count(booking_agent_id) from purchases p join ticket t using (ticket_id) \
				where p.booking_agent_id is not null and t.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'\
				group by p.customer_email\
				order by count(p.booking_agent_id) desc\
				limit 5"
		cursor.execute(query2.format(airline_name, before_day2, before_day1))
		data = cursor.fetchall()
		x1 = [i[0] for i in data]
		y1 = [int(i[1]) for i in data]
		print(before_day2, before_day1, file=sys.stdout)
		print(data, file=sys.stdout)
		print(x1, y1, file=sys.stdout)
		query = "Select p.customer_email, count(booking_agent_id) from purchases p join ticket t using (ticket_id) \
				where p.booking_agent_id is not null and t.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'\
				group by p.customer_email\
				order by count(p.booking_agent_id) desc\
				limit 5"
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=12)).strftime("%Y-%m-%d")
		cursor.execute(query.format(airline_name, before_day2, before_day1))
		data = cursor.fetchall()
		#print(spending_graph, file=sys.stdout)
		x2 = [i[0] for i in data]
		y2 = [int(i[1]) for i in data]
		print(before_day2, before_day1, file=sys.stdout)
		print(data, file=sys.stdout)
		print(x2, y2, file=sys.stdout)
		query3 = "Select p.booking_agent_id, sum(f.price)/10 from purchases p join ticket t using (ticket_id) join flight f using (flight_num) \
					where t.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\' and p.booking_agent_id is not Null\
					group by p.booking_agent_id\
					order by sum(f.price) desc\
					limit 5"
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now() - relativedelta(months=12)).strftime("%Y-%m-%d")
		cursor.execute(query3.format(airline_name, before_day2, before_day1))
		data = cursor.fetchall()
		# print(spending_graph, file=sys.stdout)
		x3 = [i[0] for i in data]
		y3 = [int(i[1]) for i in data]
		print(before_day2, before_day1, file=sys.stdout)
		print(data, file=sys.stdout)
		print(x3, y3, file=sys.stdout)
		conn.commit()
		cursor.close()
		return render_template('viewagentsStaff.html', username = username, x1=x1, x2=x2, y1=y1, y2=y2, x3=x3, y3=y3, title1 = "Top 5 Agents in Total Ticket Sales in the Past Month", title2 = "Top 5 Agents in Total Ticket Sales in the Past Year", title3 = "Top 5 Agents in Total Commission in the Past Year", max_val1 = int(float(max(y1))+2), max_val2 = int(float(max(y2))+2), max_val3 = int(float(max(y3))+100))
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")




@app.route('/frequentcustomerStaff', methods=['GET', 'POST'])
def frequentcustomerStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		test = "select airline_name from airline_staff where username = \'{}\'"
		cursor.execute(test.format(username))
		airline_name = cursor.fetchone()
		airline_name = airline_name[0]
		query = "Select c.name, p.customer_email, count(distinct ticket_id) from purchases p join customer c on c.email = p.customer_email join ticket t using (ticket_id)\
				where t.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'\
				group by p.customer_email\
				order by count(ticket_id) desc\
				limit 3"
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=12)).strftime("%Y-%m-%d")
		cursor.execute(query.format(airline_name, before_day2, before_day1))
		data = cursor.fetchall()
		conn.commit()
		cursor.close()
		return render_template('frequentcustomerStaff.html', username = username, data = data)
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")




@app.route('/takenStaff', methods=['GET', 'POST'])
def takenStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']
		email = request.form['email']
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		test = "select airline_name from airline_staff where username = \'{}\'"
		cursor.execute(test.format(username))
		airline_name = cursor.fetchone()
		airline_name = airline_name[0]
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=3)).strftime("%Y-%m-%d")
		query2 = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
					from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
					where f.airline_name = \'{}\' and f.arrival_time <= \'{}\' and p.customer_email = \'{}\'\
					order by f.departure_time desc"
		cursor.execute(query2.format(airline_name, before_day1, email))
		data = cursor.fetchall()
		conn.commit()
		cursor.close()
		return render_template('takenStaff.html', username = username, data = data)
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")



@app.route('/reportsStaff', methods=['GET', 'POST'])
def reportsStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']
		if request.method == "POST":
			before_day1 = request.form['end_date']
			before_day2 = request.form["start_date"]
			start_date = datetime.datetime.strptime(before_day2,"%Y-%m")
			end_date = datetime.datetime.strptime(before_day1,"%Y-%m")
			cursor = conn.cursor()
			test = "select airline_name from airline_staff where username = \'{}\'"
			cursor.execute(test.format(username))
			airline_name = cursor.fetchone()
			airline_name = airline_name[0]
			query2 = "select year(g.purchase_date), month(g.purchase_date), count(distinct g.ticket_id) from \
					(SELECT distinct t.ticket_id, t.airline_name, f.flight_num, f.price, p.purchase_date \
					from flight f join ticket t using (flight_num) join purchases p using (ticket_id)) g \
					where g.airline_name = \'{}\' and g.purchase_date >= \'{}\' and g.purchase_date < \'{}\'\
					group by year(g.purchase_date), month(g.purchase_date)\
					order by year(g.purchase_date) desc, month(g.purchase_date) desc"
			cursor.execute(query2.format(airline_name, start_date.strftime("%Y-%m-%d"), (end_date+relativedelta(months=1)).strftime("%Y-%m-%d")))
			report_graph = cursor.fetchall()
			months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
			print(before_day2, before_day1, months, file=sys.stdout)
			print(report_graph, file=sys.stdout)
			x_date = [(start_date+relativedelta(months=i)).strftime("%Y-%m") for i in range(months+1)]
			report_date = [datetime.date(int(i[0]), int(i[1]), 1).strftime("%Y-%m") for i in report_graph]
			print(report_date, file=sys.stdout)
			spending_s = [i[2] for i in report_graph]
			y_spending = [spending_s[report_date.index(i)] if i in report_date else 0 for i in x_date]
			#print(x_date, file=sys.stdout)
			#print(y_spending, file=sys.stdout)
			conn.commit()
			cursor.close()
			return render_template('reportsStaff.html', username = username, total=int(float(sum(y_spending))), labels=x_date, values=y_spending, title1 = "Number of Ticket Sold From "+str(x_date[0])+" to "+str(x_date[-1])+":",title2 = "Number of Ticket Sold From "+str(x_date[0])+" to "+str(x_date[-1]), max_val = int(float(max(y_spending))+2))
			#cursor.close()
			#return render_template('search.html')
		cursor = conn.cursor()
		before_day1 = (datetime.datetime.now()).strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=6)).strftime("%Y-%m-%d")
		test = "select airline_name from airline_staff where username = \'{}\'"
		cursor.execute(test.format(username))
		airline_name = cursor.fetchone()
		airline_name = airline_name[0]
		query2 = "select year(g.purchase_date), month(g.purchase_date), count(distinct g.ticket_id) from \
				(SELECT distinct t.ticket_id, t.airline_name, f.flight_num, f.price, p.purchase_date \
				from flight f join ticket t using (flight_num) join purchases p using (ticket_id)) g \
				where g.airline_name = \'{}\' and g.purchase_date >= \'{}\' and g.purchase_date <= \'{}\'\
				group by year(g.purchase_date), month(g.purchase_date)\
				order by year(g.purchase_date) desc, month(g.purchase_date) desc"
		cursor.execute(query2.format(airline_name, before_day2, before_day1))
		report_graph = cursor.fetchall()
		months = 6
		print(before_day2, before_day1, months, file=sys.stdout)
		print(report_graph, file=sys.stdout)
		x_date = [(datetime.datetime.strptime(before_day2, "%Y-%m-%d")+relativedelta(months=i)).strftime("%Y-%m") for i in range(months+1)]
		report_date = [datetime.date(int(i[0]), int(i[1]), 1).strftime("%Y-%m") for i in report_graph]
		print(report_date, file=sys.stdout)
		spending_s = [i[2] for i in report_graph]
		y_spending = [spending_s[report_date.index(i)] if i in report_date else 0 for i in x_date]
		#print(x_date, file=sys.stdout)
		#print(y_spending, file=sys.stdout)
		conn.commit()
		cursor.close()
		return render_template('reportsStaff.html', username = username, total=int(float(sum(y_spending))), labels=x_date, values=y_spending, title1 = "Number of Ticket Sold in Six Months: ",title2 = "Number of Ticket Sold in Six Months", max_val = int(float(max(y_spending))+2))
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")



@app.route('/revenueStaff', methods=['GET', 'POST'])
def revenueStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		test = "select airline_name from airline_staff where username = \'{}\'"
		cursor.execute(test.format(username))
		airline_name = cursor.fetchone()
		airline_name = airline_name[0]
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=1)).strftime("%Y-%m-%d")
		query_i1 = "Select sum(f.price) from purchases p join ticket t using (ticket_id) join flight f using (flight_num) \
					where p.booking_agent_id is not null and f.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'"
		cursor.execute(query_i1.format(airline_name, before_day2, before_day1))
		data_i1 = cursor.fetchone()
		value_i1 = data_i1[0]
		print(before_day2, before_day1, file=sys.stdout)
		print(data_i1, file=sys.stdout)
		print(value_i1, file=sys.stdout)
		query_d1 = "Select sum(f.price) from purchases p join ticket t using (ticket_id) join flight f using (flight_num) \
					where p.booking_agent_id is null and f.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'"
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=1)).strftime("%Y-%m-%d")
		cursor.execute(query_d1.format(airline_name, before_day2, before_day1))
		data_d1 = cursor.fetchone()
		#print(spending_graph, file=sys.stdout)
		value_d1 = data_d1[0]
		print(before_day2, before_day1, file=sys.stdout)
		print(data_d1, file=sys.stdout)
		print(value_d1, file=sys.stdout)
		pie_1 = [[value_i1, "Indirect Sales", "#6495ED"], [value_d1, "Direct Sales", "#DE3163"]]

		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now() - relativedelta(months=12)).strftime("%Y-%m-%d")
		query_i12 = "Select sum(f.price) from purchases p join ticket t using (ticket_id) join flight f using (flight_num) \
					where p.booking_agent_id is not null and f.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'"
		cursor.execute(query_i12.format(airline_name, before_day2, before_day1))
		data_i12 = cursor.fetchone()
		value_i12 = data_i12[0]
		print(before_day2, before_day1, file=sys.stdout)
		print(data_i12, file=sys.stdout)
		print(value_i12, file=sys.stdout)
		query_d12 = "Select sum(f.price) from purchases p join ticket t using (ticket_id) join flight f using (flight_num) \
					where p.booking_agent_id is null and f.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'"
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now() - relativedelta(months=12)).strftime("%Y-%m-%d")
		cursor.execute(query_d12.format(airline_name, before_day2, before_day1))
		data_d12 = cursor.fetchone()
		# print(spending_graph, file=sys.stdout)
		value_d12 = data_d12[0]
		print(before_day2, before_day1, file=sys.stdout)
		print(data_d12, file=sys.stdout)
		print(value_d12, file=sys.stdout)
		pie_2 = [[value_i12, "Indirect Sales", "#6495ED"], [value_d12, "Direct Sales", "#DE3163"]]
		conn.commit()
		cursor.close()
		return render_template('revenueStaff.html', username = username, x1=pie_1, x2=pie_2, title1 = "Revenue Comparison for The Past Month", title2 = "Revenue Comparison for the Past Year", max_val1 = int(float(pie_1[0][0])+100), max_val2 = int(float(pie_2[0][0])+100))
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")





@app.route('/destinationStaff', methods=['GET', 'POST'])
def destinationStaff():
	try:
		username = session['username']
		identity = session["identity"]
	except:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="You have logged out. Please log in again.")
	if identity == "staff":

		username = session['username']
		# cursor = conn.cursor()
		# year = datetime.datetime.now().strftime("%Y")
		# this_year = datetime.datetime.strptime(year+"-01-01","%Y-%m-%d")
		# last_year = datetime.datetime.strptime(str(int(year)-1)+"-01-01","%Y-%m-%d")
		# query = "select sum(g.price) from \
		# 		(SELECT distinct f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
		# 		from flight f join ticket using (flight_num) join purchases p using (ticket_id) WHERE p.customer_email = \'{}\') g \
		# 		where g.departure_time >= \'{}\' and g.departure_time < \'{}\'"
		# cursor.execute(query.format(username, last_year, this_year))
		# total_spending = cursor.fetchone()
		# if len(total_spending) == 0:
		# 	total_spending = 0
		# else:
		# 	total_spending = total_spending[0]
		# conn.commit()
		# cursor.close()
		cursor = conn.cursor()
		test = "select airline_name from airline_staff where username = \'{}\'"
		cursor.execute(test.format(username))
		airline_name = cursor.fetchone()
		airline_name = airline_name[0]
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=3)).strftime("%Y-%m-%d")
		query2 = "SELECT a.airport_city, count(t.ticket_id) from flight f join ticket t using (flight_num) join purchases p using (ticket_id) join airport a on f.arrival_airport = a.airport_name \
				where f.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'\
				group by a.airport_city\
				order by count(distinct t.ticket_id) desc\
				limit 3"
		cursor.execute(query2.format(airline_name, before_day2, before_day1))
		data = cursor.fetchall()
		x1 = [i[0] for i in data]
		y1 = [int(i[1]) for i in data]
		print(before_day2, before_day1, file=sys.stdout)
		print(data, file=sys.stdout)
		print(x1, y1, file=sys.stdout)
		query = "SELECT a.airport_city, count(t.ticket_id) from flight f join ticket t using (flight_num) join purchases p using (ticket_id) join airport a on f.arrival_airport = a.airport_name \
				where f.airline_name = \'{}\' and p.purchase_date >= \'{}\' and p.purchase_date <= \'{}\'\
				group by a.airport_city\
				order by count(distinct t.ticket_id) desc\
				limit 3"
		before_day1 = datetime.datetime.now().strftime("%Y-%m-%d")
		before_day2 = (datetime.datetime.now()-relativedelta(months=12)).strftime("%Y-%m-%d")
		cursor.execute(query.format(airline_name, before_day2, before_day1))
		data = cursor.fetchall()
		#print(spending_graph, file=sys.stdout)
		x2 = [i[0] for i in data]
		y2 = [int(i[1]) for i in data]
		print(before_day2, before_day1, file=sys.stdout)
		print(data, file=sys.stdout)
		print(x2, y2, file=sys.stdout)
		conn.commit()
		cursor.close()
		return render_template('destinationStaff.html', username = username, x1=x1, x2=x2, y1=y1, y2=y2, title1 = "Top 3 Popular Destinations for The Past three Months", title2 = "Top 3 Popular Destinations for the Past Year", max_val1 = int(float(max(y1))+2), max_val2 = int(float(max(y2))+1))
		#cursor.close()
		#return render_template('search.html')
	else:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		query = "SELECT distinct f.airline_name, f.flight_num, a.airport_city,f.departure_airport, f.departure_time,b.airport_city, f.arrival_airport, f.arrival_time, f.price, f.status, f.airplane_id \
				from flight f join ticket using (flight_num) join purchases p using (ticket_id) JOIN airport a on a.airport_name=f.departure_airport JOIN airport b on b.airport_name=f.arrival_airport\
				WHERE f.departure_time > \'{}\'\
				order by f.departure_time"
		cursor = conn.cursor()
		cursor.execute(query.format(now))
		data = cursor.fetchall()
		query = "select distinct airport_city from airport"
		cursor.execute(query)
		city = cursor.fetchall()
		city = [i[0] for i in city]
		conn.commit()
		cursor.close()
		return render_template('index.html', city=city, data=data, error="Invalid Identity. Please return.")



#Logout
@app.route('/logout')
def logout():
	session.pop("username")
	session.pop("identity")
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
