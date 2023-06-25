import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from .models import Menu,User,Transactions,Orders
from . import db
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)

UPLOAD_FOLDER = './restaurant/static/images/menu_img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route("/menu")
def mymenu():
    menus = Menu.query.all()
    print("Please add , edit or delete menu")
    return render_template("mymenu.html", menus=menus)

@admin.route("/base")
def dashboard():
    print("Welcome to admin dashboard")

    #retrieves a count of all the confirmed transactions from the "Transactions" table
    orders = Transactions.query.filter(Transactions.payment_method.is_not("None")).count()
    print(f"Total there are {orders} orders from the customer")
    
    #count of all the users from the "User" table where the "role" column is equal to the string "Customer"
    users = User.query.filter(User.role.is_("Customer")).count()
    print(f"There are total {users} registered in our platform")
    
    query = None
    total_sales = 0
    
    # joins the "Orders", "Menu", and "Transactions"
    # the "menu_id" column in the "Orders" table should match the "id" column in the "Menu" table
    # the "trxid" column in the "Orders" table should match the "id" column in the "Transactions" table
    # filter the the "payment_method" column in the "Transactions" table is not "None"
    query = db.session.query(Orders, Menu, Transactions)\
        .join(Menu, Orders.menu_id == Menu.id)\
        .join(Transactions, Orders.trxid == Transactions.id)\
        .filter(Transactions.payment_method.isnot("None"))
    
    # q=Orders , s=Menu , z=Transactions 
    for q,s,z in query:
        #print(q.quantity,s.priceperunit, z.payment_method)
        total_sales = total_sales + (q.quantity*s.priceperunit)
    print(f"Total sales is RM{total_sales}")
    return render_template("index.html" , total_orders = orders, total_customers = users,total_sales=total_sales)


@admin.route("/admin_settings")
def admin_settings():
    print("Admin settings page")
    return render_template("settings.html", currentusername = session['username'], currentuserid = session['user_id'])

@admin.route('/admin/change_credentials/<int:currentuserid>', methods=['POST'])
def change_credentials(currentuserid):
    # currentusername = session['username']
    adminusr = request.form.get('username')
    user = User.query.get(currentuserid)
   
    password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha1', salt_length=8)

    
    # check whether usernamame exist
    tempuser = User.query.filter_by(username=adminusr).first()


    if tempuser is not None:
        if user.id != tempuser.id:
            flash('Username already taken')
            print("Try a different username")
            return redirect(url_for('admin.admin_settings'))

    if user.username != adminusr:
        user.username = adminusr
    
    user.password = password
    db.session.commit()
    print("Successfully you have changed your username and password")
    print("Login using your new username and password")
    return redirect(url_for('main.index'))


@admin.route("/add_menu")
def add_menu():
    print("Adding a new menu")
    return render_template("menu_form.html")

#UPLOAD_FOLDER = './restaurant/static/images/menu_img'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
@admin.route('/add_menu', methods=['POST'])
def add_post():
    menuname = request.form.get('menuname')
    price = request.form.get('price')
    menu_type = request.form.get('menu_type')
    menu_desc = request.form.get('menu_desc')
    img = request.form.get('img')

    #since im using required in html forms , this doesn't affect
    if 'img' not in request.files:
        flash('No file part')
        return redirect(url_for('admin.add_menu'))    
    file = request.files['img']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('admin.add_menu'))
    

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
            
        new_menu = Menu( menuname=menuname, priceperunit=price,  menutype=menu_type, fooddescription=menu_desc, imagelocation = file.filename)
        db.session.add(new_menu)
        db.session.commit()
        print("Successfully menu added")
        return redirect(url_for('admin.mymenu'))
    else:
        print("try again")
        return redirect(url_for('admin.add_menu'))


@admin.route("/edit_menu/<int:menu_id>")
def edit_menu(menu_id):
    menu = Menu.query.get(menu_id)
    print("Edit menu")
    return render_template("edit_menu.html", menu = menu)

@admin.route('/edit_menu/<int:menu_id>', methods=['POST'])
def edit_menu_item(menu_id):
    menu = db.session.query(Menu).get(menu_id)
    img = request.form.get('img')
    menu.menuname = request.form.get('menuname')
    menu.priceperunit = request.form.get('price')
    menu.menutype = request.form.get('menu_type')
    menu.fooddescription = request.form.get('menu_desc')
    if 'img' in request.files:
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            menu.imagelocation = file.filename
    db.session.commit()
    print("Successfully edited menu")

    return redirect(url_for('admin.mymenu'))


# Route for deleting a menu
@admin.route('/admin/delete_menu/<int:menu_id>', methods=['GET', 'POST'])
def delete_menu(menu_id):
    menu = Menu.query.get(menu_id)

    if menu:
        db.session.delete(menu)
        db.session.commit()
        print(f"Menu deleted , {menu}")
        return redirect(url_for('admin.mymenu'))  # Redirect to the menu list page after deletion
    else:
        return "Menu not found"
    

@admin.route("/trackorders")
def trackorders():
    confirmed_transactions = Transactions.query \
    .join(User, Transactions.customer_id == User.id) \
    .filter(Transactions.payment_method != "None") \
    .all()
    print(f"Confirmed transactions by customers :{confirmed_transactions}")
    return render_template("track_orders.html", orders = confirmed_transactions)
