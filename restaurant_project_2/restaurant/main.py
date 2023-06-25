from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print("Welcome to Dine Deilgths")
    return render_template('main_page.html')

# @main.route('/admin_page')
# def admin():
#     return render_template('main_admin.html')

# @main.route('/customer_page')
# def customer():
#     return render_template('main_page_customer.html')



# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)