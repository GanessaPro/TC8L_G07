from flask_login import UserMixin
from . import login_manager, db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key =True)
    fullname = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    phonenum = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(100))

    # ONE to ONE
    # One Customer -- ONE Transaction
    transactions = db.relationship('Transactions', backref = 'users', uselist = False)

    def get_id(self):
        # this matches what user_loader needs to uniquely load a user
        return self.id

    def __init__(self, fullname, username, password, email, phonenum, gender, role):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.email = email
        self.phonenum = phonenum
        self.gender = gender
        self.role = role

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    trxid = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    quantity =db.Column(db.Integer, nullable=False)

    def __init__(self, trxid, menu_id, quantity):
        self.trxid = trxid
        self.menu_id = menu_id
        self.quantity = quantity
        

class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payment_method =db.Column(db.String, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    delivery_address =db.Column(db.String(255), nullable=False)
    # ONE to ONE
    # One Transaction -- Many Orders
    order = db.relationship('Orders', backref = 'transactions', lazy = 'dynamic')

    def __init__(self, customer_id, payment_method, order_date, delivery_address):
        self.customer_id = customer_id
        self.payment_method = payment_method
        self.order_date = order_date
        self.delivery_address = delivery_address

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    menuname = db.Column(db.String(60), nullable=False)
    priceperunit = db.Column(db.Float, nullable=False)
    menutype = db.Column(db.String(60), nullable=False)
    fooddescription = db.Column(db.Text, nullable=False)
    imagelocation = db.Column(db.String, nullable=False)
    
    # ONE to MANY
    # One Menu to Many Orders
    orders = db.relationship('Orders', backref = 'menus', lazy = 'dynamic')

    def __init__(self, menuname, priceperunit, menutype, fooddescription, imagelocation):
        self.menuname = menuname
        self.priceperunit = priceperunit
        self.menutype = menutype
        self.fooddescription = fooddescription
        self.imagelocation = imagelocation
    
    def __repr__(self):
        return f'Food item: {self.id} is {self.menuname}, price per unit is {self.priceperunit}, menutype is {self.menutype}, description is {self.fooddescription}.'


@login_manager.user_loader
def load_user(id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(id))