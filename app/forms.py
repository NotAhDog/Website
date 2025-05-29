from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import Optional, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=5,
                                              max=20,
                                              message="Enter something between 5 and 20 characters")],
                           render_kw={"placeholder": "Username..."}
                           )

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8,
                                                max=25,
                                                message="Enter something between 8 and 25 characters")],            
                             render_kw={"placeholder": "Password..."},
                             )

    # Note: the string you pass in here is how you label the button
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=5,
                                              max=20,
                                              message="Enter a something between 5 and 20 characters")],
                           render_kw={"placeholder": "Enter a username..."}
                           )

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8,
                                                max=25,
                                                message="Enter something between 8 an 25 characters")],
                             render_kw={"placeholder": "Enter a password..."}
                             )

    confirmpass = PasswordField('Repeat Your Password',  # Making sure they entered the correct password
                                validators=[DataRequired(),
                                            EqualTo('password', message="These passwords dont match"),
                                            Length(min=8,
                                                   max=25,
                                                   message="Enter something that matches the password and is between 8 and 25 characters")],
                                render_kw={"placeholder": "Repeat the password..."}
                                )

    submit = SubmitField('Submit')
