from flask import *
from flask_sqlalchemy import *
import qrcode

#make qr code
website_url = "http://127.0.0.1:5000"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(website_url)
qr.make(fit=True)
img = qr.make_image(fill="black", back_color="white")
img.save("qr_code.png")

#make app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotelMenu.db'
db = SQLAlchemy(app)

class Menu(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(length=30), nullable=False)
    name =  db.Column(db.String(length=30), nullable=False)
    price = db.Column(db.Integer(), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    orderid = db.Column(db.Integer(), nullable=False)
    ordernos = db.Column(db.Integer(), nullable=False)
    ordername =  db.Column(db.String(length=30), nullable=False)
    orderprice = db.Column(db.Integer(), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('renderMenu'))

@app.route('/add_menu_item')
def add_menu_item():
    item = Menu(category="Chinese Food", name="Mapo Tofu", price=180)
    db.session.add(item)
    db.session.commit()
    return "Item added successfully!"

@app.route('/renderMenu')
def renderMenu():
    menu = Menu.query.all()
    categories = {}
    for item in menu:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    return render_template('renderMenu.html', categories=categories)

@app.route('/add_order', methods=['POST'])
def add_order():
    orderid = request.form.get('orderid')
    ordernos = request.form.get('ordernos')
    ordername = request.form.get('ordername')
    orderprice = request.form.get('orderprice')
    existing_order = Order.query.filter_by(orderid=orderid).first()
    if not existing_order:
        orderitem = Order(orderid=orderid, ordername=ordername, ordernos=ordernos, orderprice=orderprice)
        db.session.add(orderitem)
        db.session.commit()
    else:
        existing_order.ordernos = ordernos
        db.session.commit()
    return redirect(url_for('renderMenu'))

@app.route('/renderBill')
def renderBill():
    orders = Order.query.all()
    total_amount = 0
    for order in orders:
        total_amount += order.ordernos * order.orderprice
    return render_template('renderBill.html', orders=orders, total_amount=total_amount)

@app.route('/renderBillRequest')
def renderBillRequest():
    return redirect(url_for('renderBill'))


if __name__ == '__main__':
    app.run(debug=True)