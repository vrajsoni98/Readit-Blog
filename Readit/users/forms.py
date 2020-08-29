#users/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from Readit.models import User


class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit=SubmitField('Login')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired(),Length(min=3, max=20,message="Username must be 3 to 20 characters long")])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Password must Match'),Length(min=8, max=128, message='Password must be of 8 characters atleast')])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Register')


    def check_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Your Email has already been Registered!")

    def check_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username is already taken!")

class UpdateUserForm(FlaskForm):

    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired(),Length(min=3, max=20,message="Username must be 3 to 20 characters long")])
    picture=FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def check_email(self, email):
        if username.data != current_user.username:
        #if updated username is same as old one or it isnt changed then we dont need to check further
            if User.query.filter_by(email=self.email.data).first():
                raise ValidationError("Your Email has already been Registered!")

    def check_username(self, username):
        if email.data != current_user.email:
            if User.query.filter_by(username=self.username.data).first():
                raise ValidationError("Username is already taken!")
