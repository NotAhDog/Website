from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# This must come last to avoid circular import
from app import routes

app.run(debug=True)
