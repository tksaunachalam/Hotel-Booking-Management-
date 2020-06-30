from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length , Email, EqualTo, ValidationError
from HotelBooking.models import User
from flask import flash


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)] )

    email = StringField('Email',
                         validators=[DataRequired(), Email()] )

    password = PasswordField('Password',validators=[DataRequired()] )
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password') ] )

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('username already taken', 'success')
            #raise ValidationError('That username is already taken choose a new name')
            raise ValidationError("uname taken")

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken choose a new name')



class LoginForm(FlaskForm):
    email = StringField('Email',
                         validators=[DataRequired(), Email()] )

    password = PasswordField('Password',validators=[DataRequired()] )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class BookingForm(FlaskForm):
    CheckIn = StringField('CheckIn',id='datepicker',validators=[DataRequired()])
    #CheckIn = DateField('CheckIn',validators=[DataRequired()])
    CheckOut = StringField(id='datepicker2')
    Adults = StringField('Adults')
    Kids = StringField('Kids')
    Search = SubmitField('Search Availability')


class EnquiryForm(FlaskForm):
    Name = StringField('Name',validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()] )
    Msg = StringField('Message', validators=[DataRequired()])
    Submit = SubmitField('Send Message')

class ConfirmBooking(FlaskForm):
    Submit = SubmitField('Book')
    ModeOfPayment = SelectField('Select Payment Method',choices=[('card','Card'),('cash','Cash')])
    Cancel = SubmitField('Cancel')

class AmenityForm(FlaskForm):
    Amenities = SelectMultipleField('Select Amenities if required', choices=[('4','Extra-Bed'),('5','PlayStation'),('6','dog-care'),('7','spa'),('8','laundry')])
