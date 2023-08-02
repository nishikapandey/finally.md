from flask import Flask, render_template, request, url_for, redirect
# import pymysql
import mysql.connector
from dotenv import load_dotenv
import os

# Secure MYSQL Password
load_dotenv()
db_password = os.getenv('DB_PASSWORD')

# Establish a connection to the MySQL database
connector = mysql.connector.connect(
    host='localhost',
    user='root',
    password=db_password,
    database='customers_new'
)

# Create a cursor object to execute SQL queries
cursor = connector.cursor()
# Execute a SELECT query - For Countries
query = "SELECT name FROM countries"
cursor.execute(query)
rows = cursor.fetchall()
countries = []
for row in rows:
    countries.append(row[0])

# Execute a SELECT query - For States
# query = "SELECT name FROM states"
query = "select name from states where country_id in (select id from countries where name=%s)"
cursor.execute(query,  ("India",))
rows = cursor.fetchall()
states = []
for row in rows:
    states.append(row[0])

# Execute a SELECT query - For Cities
# query = "SELECT name FROM cities order by name"
query = "select name from cities where state_id=4039"
cursor.execute(query)
rows = cursor.fetchall()
cities = []
for row in rows:
    cities.append(row[0])

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def page1():
    if request.method == 'POST':   
        # student details
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        name = first_name + " " + last_name
        age = request.form['applicant_age']
        education = request.form['applicant_education']
        aadhar_number = request.form['applicant_aadhar']
        # contact details
        primary_mobile = request.form['primary_no']
        secondary_mobile = request.form['secondary_no']
        primary_email = request.form['primary_email']
        secondary_email = request.form['secondary_email']
        # address details
        c_address = request.form['c_address']
        c_country = request.form['c_country']
        c_state = request.form['c_state']
        c_city = request.form['c_city']
        p_address = request.form['p_address']
        p_country = request.form['p_country']
        p_state = request.form['p_state']
        p_city = request.form['p_city']
        # Course details 
        course = request.form['applicant_course']
        referral = request.form['applicant_referral']
        availability = request.form['applicant_availability']
        councellor = request.form['applicant_councellor']
     
        # Queries for STUDENT_INFO TABLE
        sql = "INSERT INTO student_info (NAME, AGE , EDUCATION, AADHAR_NO) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (name, age, education, aadhar_number))
        connector.commit()
        # Queries for CONTACT_INFO TABLE
        sql = "INSERT INTO contact_info (MOBILE_01, MOBILE_02, EMAIL_01, EMAIL_02) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (primary_mobile, secondary_mobile, primary_email, secondary_email))
        connector.commit()
        # Queries for ADDRESS_INFO TABLE
        sql = "INSERT INTO address_info (P_ADD, P_CITY, P_STATE, P_COUNTRY, C_ADD, C_CITY, C_STATE, C_COUNTRY ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (p_address, p_city, p_state, p_country, c_address, c_city, c_state, c_country))
        connector.commit()
        # Queries for COURSE_INFO TABLE
        # sql = "INSERT INTO course_info (COURSE_ID, COURSE_NAME) VALUES (%s,%s)"
        sql = "INSERT INTO course_info (COURSE_NAME, REFERRAL, AVAILABILITY, COUNCELLOR) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (course, referral, availability, councellor))
        connector.commit()

        return render_template ('enquiry_submission.html' , fname = name)
        # return redirect("https://bignalytics.in/")
    if request.method=="GET":
        return render_template('enquiry_form.html', countries=countries, cities=cities , states=states)

# Below code is for field wise data capture before submission of complete form.
@app.route('/capture-country', methods=['POST'])
def capture_country():
    # global country_value
    country_value = request.form.get("applicant_country")
    query = "select name from states where country_id in (select id from countries where name=%s)"
    cursor.execute(query,  (country_value,))
    rows = cursor.fetchall()
    for row in rows:
        states.append(row[0])
        print(country_value)
        return 'Field1 captured successfully!'

@app.route('/capture-states', methods=['POST'])
def capture_states():
    state_value = request.form.get("applicant_state")
    print(state_value)
    return 'Field1 captured successfully!'


@app.route('/capture-name', methods=['POST'])
def capture_name():
    captured_name = request.form.get("applicant_name")
    print(captured_name)
    return 'Field1 captured successfully!'



# QR CODE GENERATION
# import pyqrcode
# from pyqrcode import QRCode
# s ="http://192.168.1.25:5000/"
# url = pyqrcode.create(s)
# url.png("Enquiry_form_QRCode.png", scale=8)


# OTP Verification Code
# from flask import Flask, render_template, request
# from twilio.rest import Client
# import random

# # Twilio configuration
# account_sid = 'ACcbbb4a03672511b327bb6bf4a5e702ab'
# auth_token = '44f62f25e60d4be44496f1ea1ff588e8'
# twilio_number = '+19513388877'

# # Route to send OTP
# @app.route('/send', methods=['GET','POST'])
# def send_otp():
#     if request.method == 'GET':
#         return render_template("index.html")
    
#     if request.method == 'POST':
#         phone_number = request.form['mobile']
        
#         # Generate a random OTP
#         otp = random.randint(1000, 9999)
        
#         # Create a Twilio client
#         client = Client(account_sid, auth_token)
        
#         # Send the OTP via SMS
#         message = client.messages.create(
#             body=f'Your OTP: {otp}',
#             from_=twilio_number,
#             to=phone_number
#         )
        
#         return 'OTP sent successfully!'

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)