from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=3,
                                              max=20,
                                              message="Enter a username "
                                                      "between 3 and 20 "
                                                      "characters")],
                           render_kw={"placeholder": "Username..."}
                           )

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=5,
                                                max=25,
                                                message="Enter a password "
                                                "between 5 and 25 "
                                                "characters")],
                             render_kw={"placeholder": "Password..."},
                             )

    # Note: the string you pass in here is how you label the button
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=3,
                                              max=20,
                                              message="Enter a username "
                                              "between 3 and 20 characters")],
                           render_kw={"placeholder": "Enter a username..."}
                           )

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=5,
                                                max=25,
                                                message="Enter a password "
                                                "between 5 an 25 characters")],
                             render_kw={"placeholder": "Enter a password..."}
                             )

    confirmpass = PasswordField('Repeat Your Password',  # Making sure they
                                                         # entered the correct
                                                         # password
                                validators=[DataRequired(),
                                            EqualTo('password', message=""
                                            "These passwords don't match"),
                                            Length(min=5,
                                                   max=25,
                                                   message="Enter something "
                                                   "that matches the password "
                                                   "and is between 5 and 25 "
                                                   "characters")],
                                render_kw={"placeholder": ""
                                           "Repeat the password..."}
                                )

    submit = SubmitField('Submit')


class FeedbackForm(FlaskForm):
    look = StringField('How does the website look?',
                       validators=[DataRequired(),
                                   Length(min=3,
                                          max=50,
                                          message="Enter something between 3 "
                                          "and 50 characters")],
                       render_kw={"placeholder": ""
                                  "Do you like how the website looks?"}
                       )

    additions = StringField('Do you have any additions for the website?',
                            validators=[DataRequired(),
                                        Length(min=3,
                                               max=50,
                                               message="Enter something "
                                               "between 3 and 50 characters")],
                            render_kw={"placeholder": "Is there anything that "
                                       "could be added or changed?"}
                            )

    easytouse = RadioField(u'Is the website easy to use?',
                           validators=[DataRequired()],
                           choices=[('Not at all', 'Not at all'),
                                    ('Not really', 'Not really'),
                                    ('A little', 'A little'),
                                    ('Really easy', 'Really easy')],
                           render_kw={'class': ''}
                           )

    other = StringField('Any other feedback?',
                        validators=[Length(max=50)],
                        render_kw={"placeholder": "Other feedback"}
                        )

    submit = SubmitField('Submit')
