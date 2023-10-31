from flask import Flask, render_template, request, redirect, session, flash, jsonify
from mysqlconnection import MySQLConnector
# from __future__ import print_function
import re
import os
import json
import MySQLdb
import MySQLdb.cursors as cursors

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')
PASS_REGEX = re.compile(r'.*[A-Z].*[0-9]')

app = Flask(__name__)
mysql = MySQLConnector(app, 'twitter_data')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/UserLogin')
def user():
    return render_template('UserLogin.html')

@app.route('/Register')
def register():
    return render_template('Register.html')

@app.route('/logout')
def logout():
    return render_template('index.html')



@app.route('/changeUserPass')
def changeUserPass():
    return render_template('changeUserPass.html')

@app.route('/UserHome')
def user_home():
    return render_template('UserHome.html')

@app.route('/reg', methods=['POST'])
def register_user():
    input_email = request.form['email']
    email_query = "SELECT * FROM user WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)
    query = "INSERT INTO user (username, password, email, mob) VALUES (:name, :pass, :email_id, :mob)"
    data = {
            'name': request.form['username'],
            'email_id': request.form['email'],
            'mob': request.form['mob'],
            'pass': request.form['password']
        }

    mysql.query_db(query, data)

    input_email = request.form['email']
    email_query = "SELECT * FROM user WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)

    return render_template('UserLogin.html')



@app.route('/ulogin', methods=['POST'])
def ulogin():
    username = request.form['username']
    input_password = request.form['password']
    email_query = "SELECT * FROM user WHERE username = :uname and password = :pass"
    query_data = {'uname': str(username), 'pass':str(input_password)}
    stored_email = mysql.query_db(email_query, query_data)
    if not stored_email:
        return redirect('/')

    else:
        if request.form['password'] == stored_email[0]['password']:
            return render_template('UserHome.html')

        else:
            return redirect('/')



@app.route('/viewbehv')
def viewb():
    return render_template('view_behv.html')


if __name__ == "__main__":
    app.run(debug=True)
