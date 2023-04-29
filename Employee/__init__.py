import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
'''
for Local:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Emp_details.db' 
'''
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# postgres://postgresql_database_d71r_user:xWqs8GEPeUYeVPfiCjUC5yjNOENIB7MX@dpg-ch6f5jbhp8u9bo28ub00-a.oregon-postgres.render.com/postgresql_database_d71r
app.config['SECRET_KEY'] = '8584811b741996d5e662fd05'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from Employee import routes

