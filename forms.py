from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from wtforms.validators import Length





class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")




class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('pass_confirm', message='passwords must match!')])
    pass_confirm = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register!")

    def check_email(self, field):
        # check if the email has already been activated
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered!')

    
    def check_username(self, field):
        if User.query.field.filter_by(username=field.data).first():
            raise ValidationError("Username is taken!")




class NotesForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(max=15)])
    text = TextAreaField('Your note', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Save")





class UpdateProfile(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Update')


    def check_email(self, field):
        # check if the email has already been activated
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been already registered!')
        
    # if the username is already taken
    def check_username(self, field):
        if User.query.field.filter_by(username=field.data).first():
            raise ValidationError("Username is taken!")