from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, RadioField, PasswordField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from Employee.models import Item

# For Register page
class RegisterForm(FlaskForm):
    def validate_phone(self, phone_to_check):
        phone = Item.query.filter_by(phone=phone_to_check.data).first()
        if phone:
            raise ValidationError('Already exists Phone No. ! Please try a different Phone No.')

    def validate_Email(self, Email_to_check):
        Email = Item.query.filter_by(Email=Email_to_check.data).first()
        if Email:
            raise ValidationError('Email Address already exists! Please try a different email address')

    Firstname=StringField(label="First name:", validators=[Length(min=2, max=10), DataRequired()])
    Lastname=StringField(label="Last name:", validators=[Length(min=2, max=10), DataRequired()])
    Email=StringField(label="Email ID:", validators=[Email(), DataRequired()])
    phone=IntegerField(label="Phone no.", validators=[DataRequired()])
    Role=RadioField(label='Role:', choices=[('Admin','Admin'), ('Employee','Employee')], default=0)
    DOB=StringField(label="Date of Birth:", validators=[Length(max=10), DataRequired()])
    Address=TextAreaField(label="Address:", validators=[Length(max=20), DataRequired()])
    password1 = PasswordField(label='Password:',validators=[Length(min=5), DataRequired()] )
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit=SubmitField(label="Create Account")

# For search bar
class searchForm(FlaskForm):
    searched=StringField(label='search', validators=[DataRequired()])
    submit=SubmitField(label='search')

# For Login page
class LoginForm(FlaskForm):
    Email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')