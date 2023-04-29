from Employee import db, login_manager
from flask_login import UserMixin

# Load user
@login_manager.user_loader
def load_user(user_id):
    return Item.query.get(int(user_id))

# Model
class Item(db.Model, UserMixin):
    id=db.Column(db.Integer(), primary_key=True)
    Firstname=db.Column(db.String(length=20), nullable=False)
    Lastname=db.Column(db.String(length=20), nullable=False)
    Email=db.Column(db.String(length=20), nullable=False, unique=True)
    phone=db.Column(db.BigInteger(), nullable=False, unique=True)
    DOB=db.Column(db.String(length=10), nullable=False)
    Address=db.Column(db.String(length=20), nullable=False)
    Role=db.Column(db.String(), nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)

    # def __repr__(self):
    #     return f'Item{self.name}'