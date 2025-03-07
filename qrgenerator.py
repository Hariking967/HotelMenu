from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotelMenu.db'
db = SQLAlchemy(app)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, nullable=False)
    ordernos = db.Column(db.Integer, nullable=False)
    ordername = db.Column(db.String(30), nullable=False)
    orderprice = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return redirect(url_for('renderMenu'))

@app.route('/renderMenu')
def renderMenu():
    menu = Menu.query.all()
    categories = {}
    for item in menu:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    return render_template('renderMenu.html', categories=categories)

@app.route('/renderBill')
def renderBill():
    orders = Order.query.all()
    total_amount = sum(order.ordernos * order.orderprice for order in orders)
    return render_template('renderBill.html', orders=orders, total_amount=total_amount)

# Vercel requires this to work
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(debug=True)
