from flask import Flask, request, render_template, url_for, redirect
from customer import sign_up, log_in
from db_init import init
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        print(log_in(db, dict(request.form)))
        return redirect(url_for('/'))
       
    return render_template('login.html', msg=msg)

@app.route('/createAccount', methods =['GET', 'POST'])
def createAccount():
    msg = ''
    if request.method == 'POST':
        sign_up(db, dict(request.form))
        # TODO: show sing up successful message
        return redirect(url_for('login'))
    
    return render_template('createAccount.html', msg = msg)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == "__main__":
    db = init() # use your own db initialization
    app.run(debug=True)

