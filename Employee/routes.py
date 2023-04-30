import flask_login
from Employee import app
from flask import render_template, redirect, url_for, flash, request
from Employee.models import Item
from Employee.Forms import RegisterForm, LoginForm, searchForm
from Employee import db, bcrypt
from sqlalchemy import func
from flask_login import login_user, logout_user, current_user

# Home page
@app.route('/')
@app.route('/homepage')
def home_page():
    return render_template('home.html')

# Employee Details
@app.route('/Emp_details')
def Emp_details():
    items = Item.query.all()
    if current_user.is_authenticated:
        if current_user.Role == 'Admin':
            return render_template('Emp_details.html', items=items)
        else:
            return render_template('Individual_details.html')
    return redirect(url_for('home_page'))

# Individual Employee Details
@app.route('/Individual_details')
def Individual_details():
    items = Item.query.all()
    if current_user.is_authenticated:
        if current_user.Role == 'Admin':
            return render_template('Emp_details.html', items=items)
        else:
            return render_template('Individual_details.html')
    return redirect(url_for('home_page'))

# Search Page
@app.route('/Emp_details/search', methods=['GET','POST'])
def search_page():
    form = searchForm()
    if form.validate_on_submit:
        searched = form.searched.data
        query_a = Item.query.filter(func.CONCAT(Item.Firstname," ", Item.Lastname," ", Item.Address).like('%'+searched+'%'))
        return render_template('Search.html', form=form, searched=searched, query_a=query_a)
    return render_template('Search.html', form=form)

# Registration Page
@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        encrypted_password=bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user_to_create=Item(Firstname=form.Firstname.data, Lastname=form.Lastname.data,
                            Email=form.Email.data, phone=form.phone.data, DOB=form.DOB.data,
                            Address=form.Address.data, Role=form.Role.data, password_hash=encrypted_password)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))

    if form.errors != {}:
       for err_msg in form.errors.values():
           flash(f'There was an error while create a user:{err_msg}', category='danger')

    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    return render_template('register.html', form=form)

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Item.query.filter_by(Email=form.Email.data).first()
        if attempted_user and bcrypt.check_password_hash(attempted_user.password_hash, form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.Firstname} {attempted_user.Lastname}', category='success')
            if attempted_user.Role == 'Employee':
                return redirect(url_for('Individual_details'))
            elif attempted_user.Role == 'Admin':
                return redirect(url_for('Emp_details'))
        else:
            flash('Email and password are not match! Please try again', category='danger')
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    return render_template('login.html', form=form)

# LogOut
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

# Update Details
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update_item(id):
    update_id=Item.query.filter_by(id=id).first()
    if request.method == 'POST':
        update_id.Firstname = request.form['Firstname']
        update_id.Lastname = request.form['Lastname']
        update_id.Email = request.form['Email']
        update_id.phone = request.form['phone']
        update_id.DOB = request.form['DOB']
        update_id.Address = request.form['Address']
        try:
            db.session.commit()
            flash(f'Update Employee Id: {id} information', category='secondary')
            return redirect(url_for('Emp_details'))
        except:
            flash(f'There was a problem Updating an employee', category='danger')
    else:
        return render_template('update.html', update_id=update_id)

# Delete Details
@app.route('/delete/<int:id>')
def delete_item(id):
    delete_id=Item.query.get_or_404(id)
    try:
        if flask_login.current_user == delete_id:
            flash(f'Already login! Sorry this action is not performed', category='danger')
            return redirect((url_for('Emp_details')))
        else:
            if delete_id.Role == 'Admin':
                flash(f'Oops! Admin role can not be Deleted', category='warning')
                return redirect((url_for("Emp_details")))
            else:
                db.session.delete(delete_id)
                db.session.commit()
                flash(f'Employee details deleted successfully', category='info')
                return redirect((url_for("Emp_details")))
    except:
         flash(f'Whoops! There was a problem', category='danger')
         return redirect((url_for("Emp_details")))