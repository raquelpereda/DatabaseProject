from flask import Flask, request, render_template 
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass123'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = %s AND password = %s', (username, password,))

        customer = cursor.fetchone()
        # If account exists in accounts table in out database
        if customer:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = customer['id']
            session['username'] = customer['username']
            # Redirect to home page
            return render_template('index.html', msg=msg)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/createAccount', methods =['GET', 'POST'])
def createAccount():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = % s', (username, ))
        customer = cursor.fetchone()
        if customer:
            msg = 'This account has already been registered. Try signing in.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address.'
        elif not username or not password or not email:
            msg = 'Required fields missing.'
        else:
            cursor.execute("INSERT INTO customers (firstname, lastname, username, password, phone) VALUES (% s, % s, % s, %s, %s)", (firstname, lastname, username, password, phone, ))
            mysql.connection.commit()
            return render_template('index.html')
    elif request.method == 'POST':
        return render_template('createAccount.html', msg = msg)




if __name__ == "__main__":
    app.run()

