from flask import Flask, request, render_template, url_for, redirect, flash
from customer import sign_up, log_in, searchClothes
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
        results = log_in(db, dict(request.form))
        if not results:
            flash('Wrong login information. Please try again.')
            return render_template('login.html')
        flash('You have been successfully logged in.')
        return redirect(url_for('index'))
       
    return render_template('login.html', msg=msg)

@app.route('/createAccount', methods =['GET', 'POST'])
def createAccount():
    msg = ''
    if request.method == 'POST':
        results = sign_up(db, dict(request.form))
        if results == '':
            flash('This account already exists.')
            return redirect(url_for('createAccount'))
        flash('You have been successfully registered.')
        return redirect(url_for('login'))
    
    return render_template('createAccount.html', msg = msg)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/searchResults')
def searchResults(result):
    return render_template('searchResults.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.form.getlist('SearchType')
        results = searchClothes(db, data)
        if not results:
            results = "No clothes were found."
        return render_template('searchResults.html', result = results)
    return render_template('search.html')

if __name__ == "__main__":
    db = init('clothing_store') # use your own db initialization
    app.secret_key = "something only you know"
    app.run(debug=True)

