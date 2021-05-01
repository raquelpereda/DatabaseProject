from flask import Flask, request, render_template, url_for, redirect, flash
from customer import *
from item import *
from cart import *
from db_init import init
import os
import json

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
        global user
        user = Customer(results)
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

@app.route('/searchResults', methods = ['GET', 'POST'])
def searchResults():
    if request.method == 'POST':
        if not user:
            return redirect(url_for('login'))        
        data = request.form.getlist('item')
        for clid in data:
            clid = clid[1:-1]
            user.cart.add_item(Item(get_item(db, clid)))
        print(user.cart.items)
        return redirect(url_for('checkout'))
    return render_template('searchResults.html', result = results)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        if not user:
            return redirect(url_for('login'))
        buy(db, user, dict(request.form)["cardNum"])
        flash('Your order has been placed')
        return redirect(url_for('index'))
    return render_template('checkout.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        global results
        # data = request.form.getlist('SearchType')
        data = {"category":[], "size":[], "color":[]}
        cat = request.form.getlist('category')
        for c in cat:
            data["category"].append(c)
        size = request.form.getlist('size')
        for s in size:
            data["size"].append(s)
        color = request.form.getlist('color')
        for cl in color:
            data["color"].append(cl)
        results = searchClothes2(db, data)
        if not results:
            results = "No clothes were found."
        return redirect(url_for('searchResults'))
    return render_template('search.html')

if __name__ == "__main__":
    db = init('test_db') # use your own db initialization
    app.secret_key = "something only you know"
    user = None
    results = None
    app.run(debug=True)

