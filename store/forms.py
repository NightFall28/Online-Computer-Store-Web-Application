from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, InputRequired
from store.models import User, EdgeComputingRAM

positionList = ['Customer', 'Employee']

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    position = SelectField('Position', validators=[DataRequired()], choices=positionList)
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=50)])
    zipcode = IntegerField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists, please use another email.')

# class RegistrationForm1(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')
        
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=50)])
    zipcode = IntegerField('Zip Code', validators=[DataRequired()])

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please choose a different one.')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class MemoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')

class WalletForm(FlaskForm):
    deposit_amount = DecimalField('Amount to Deposit', validators=[DataRequired(), NumberRange(min=0, message='Amount cannot be negative')])
    card_holder = StringField('Card Holder', validators=[DataRequired(), InputRequired()])
    card_number = StringField('Card Number', validators=[DataRequired(), InputRequired()])
    card_expire_month = SelectField('Expiry Month', choices=[(str(i), str(i)) for i in range(1, 13)], validators=[DataRequired(), InputRequired()])
    card_expire_year = SelectField('Expiry Year', choices=[(str(i), str(i)) for i in range(2023, 2030)], validators=[DataRequired(), InputRequired()])
    cvv = IntegerField('CVV', validators=[DataRequired(), InputRequired()])
    submit = SubmitField('Deposit')

class SelectProductTypeForm(FlaskForm):
    computer_type = SelectField('Type', choices=['Desktop','Laptop','Edge Computing', 'MacBook', 'iMac'], validators=[DataRequired()])
    submit = SubmitField('Select')

class AddDesktopForm(FlaskForm):
    name = StringField('Name of the Build', validators=[DataRequired()])
    category = SelectField('Category', choices=['Business','Academic','Gaming'], validators=[DataRequired()])
    motherboard = SelectField('Motherboard',coerce=str, choices=[])
    processor = SelectField('Processor', choices=[], coerce=str)
    graphic_card = SelectField('Graphic Card',coerce=str)
    operating_system = SelectField('Operating System', choices=['Windows 11', 'Linux'])
    memory = SelectField('Memory',coerce=str)
    hard_drive = SelectField('Hard Drive',coerce=str)
    case = SelectField('Case',coerce=str)
    submit = SubmitField('Add')

class AddLaptopForm(FlaskForm):
    name = StringField('Name of the Build', validators=[DataRequired()])
    category = SelectField('Category', choices=['Business','Academic','Gaming'], validators=[DataRequired()])
    processor = SelectField('Processor', choices=[])
    graphic_card = SelectField('Graphic Card',coerce=str)
    operating_system = SelectField('Operating System', choices=['Windows 11', 'Linux'])
    memory = SelectField('Memory',coerce=str)
    hard_drive = SelectField('Hard Drive',coerce=str)
    image_file = FileField('Image', validators=[InputRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

class AddEdgeComputingForm(FlaskForm):
    name = SelectField('Name', choices=[], coerce=str)
    RAM = SelectField('RAM', coerce=str)
    image_file = FileField('Image', validators=[InputRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

class AddMacbookForm(FlaskForm):
    name = SelectField('Name', choices=[])
    memory = SelectField('Memory', choices=[])
    storage = SelectField('Storage', choices=[])
    image_file = FileField('Image', validators=[InputRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

class AddiMacForm(FlaskForm):
    name = SelectField('Name', choices=[])
    color = SelectField('Color', choices=['Blue', 'Green', 'Pink', 'Silver', 'Yellow', 'Orange', 'Purple'])
    memory = SelectField('Memory', choices=[])
    storage = SelectField('Storage', choices=[])
    accessory = SelectField('Accessory', choices=[])
    image_file = FileField('Image', validators=[InputRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

class CustomizeDesktopForm(FlaskForm):
    motherboard = SelectField('Motherboard',coerce=str, choices=[])
    processor = SelectField('Processor', choices=[], coerce=str)
    graphic_card = SelectField('Graphic Card',coerce=str)
    operating_system = SelectField('Operating System', choices=['Windows 11', 'Linux'])
    memory = SelectField('Memory',coerce=str)
    hard_drive = SelectField('Hard Drive',coerce=str)
    case = SelectField('Case',coerce=str)
    submit = SubmitField('Go To Checkout')

class CustomizeLaptopForm(FlaskForm):
    processor = SelectField('Processor', choices=[], coerce=str)
    graphic_card = SelectField('Graphic Card',coerce=str)
    operating_system = SelectField('Operating System', choices=['Windows 11', 'Linux'])
    memory = SelectField('Memory',coerce=str)
    hard_drive = SelectField('Hard Drive',coerce=str)
    submit = SubmitField('Go To Checkout')

class CustomizeEdgeComputingForm(FlaskForm):
    RAM = SelectField('RAM', coerce=str)
    submit = SubmitField('Go To Checkout')

class CustomizeMacbookForm(FlaskForm):
    memory = SelectField('Memory', choices=[])
    storage = SelectField('Storage', choices=[])
    submit = SubmitField('Go To Checkout')

class CustomizeiMacForm(FlaskForm):
    color = SelectField('Color', choices=['Blue', 'Green', 'Pink', 'Silver', 'Yellow', 'Orange', 'Purple'])
    memory = SelectField('Memory', choices=[])
    storage = SelectField('Storage', choices=[])
    accessory = SelectField('Accessory', choices=[])
    submit = SubmitField('Go To Checkout')

class AddCommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Comment')

class NewCommunicateForm(FlaskForm):
    order_id = IntegerField('Order ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Send')

class CommunicateCommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')

class ContactAdminForm(FlaskForm):
    reported_user_id = IntegerField('Enter the User ID that you want to report', validators=[DataRequired()])
    content = TextAreaField('Please provide your reason', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProcessReportForm(FlaskForm):
    compliment = IntegerField('Number of Compliment', validators=[InputRequired()])
    warning = IntegerField('Number of Warning', validators=[InputRequired()])
    submit = SubmitField('Submit')

class DisplayPermissionForm(FlaskForm):
    allow = SelectField('Allow For Display?', choices=['Yes','No'])
    submit = SubmitField('Submit')

class RatingForm(FlaskForm):
    rating = SelectField('Rate This Configuration (1-Worst, 5-Best)', choices=['1','2','3','4','5'])
    submit = SubmitField('Submit')
