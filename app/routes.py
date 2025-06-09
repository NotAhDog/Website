from app import app
from flask import Flask, render_template, request
from .forms import LoginForm, SignupForm
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "database.db")
db.init_app(app)


import app.models as models
app.secret_key = 'CorrectHorseBatteryStaple'


# --- Routes ---


@app.route('/', methods=['GET', 'POST'])  # Home page
def root():
    print(request.args.get('user'))
    return render_template('home.html', page_title='HOME')


@app.route('/about')  # About page
def about():
    title = "About"
    return render_template('about.html', page_title='ABOUT', title=title)


@app.route('/folios')  # Folios page
def all_folios():
    title = "Folios"
    folios = models.Folio.query.all()
    return render_template('folios.html', folios=folios, title=title, folio_num=len(folios))


@app.route('/projects')  # projects page
def all_artists():
    title = "Projects"
    return render_template('projects.html',  title=title)


@app.route('/artwork')  # Artwork page
def all_arts():
    title = "Artwork"
    arts = models.Art.query.all()
    return render_template('artwork.html', arts=arts, title=title)


@app.route('/folios/<int:id>')
def folio(id):
    folio = models.Folio.query.options(
        db.joinedload(models.Folio.theme),
        db.joinedload(models.Folio.layouts)
    ).get_or_404(id)
    return render_template('detailfolios.html', folio=folio, arts=folio.arts)


@app.route('/artist/<int:id>')
def artist(id):
    artist = models.Artist.query.get_or_404(id)
    return render_template('artist.html', artist=artist)


@app.route('/art/<int:id>')
def art(id):
    title = "Art - <int:id>"
    art = models.Art.query.get_or_404(id)
    return render_template('art.html', art=art, meanings=art.meanings, folios=art.folios, title=title)


@app.route('/secret')  # Secret page
def secret():
    title = "Secret"
    return render_template('secret.html', title=title)


@app.route('/account', methods=['GET', 'POST'])  # Login page
def login():
    title = "Login"
    form = LoginForm()
    if request.method == "GET":
        print("\n\nLOADING PAGE\n\n")
    else:  # request.method is POST - Someone clicked submit
        if form.validate_on_submit():
            print('-------------------------------')
            print(f"Username: {form.username.data}")
            print(f"Password: {form.password.data}")
            print('-------------------------------')
            title = f"Hello, {form.username.data}"
        else:  # a validator failed... lets see which one(s)
            print('-------------------------------')
            print('ERROR:')
            print(form.errors)
            print('-------------------------------')
    return render_template('login.html', form=form, title=title)


@app.route('/signup', methods=['GET', 'POST'])  # Signup page
def signup():
    title = "Signup"
    form = SignupForm()
    if request.method == "GET":
        print("\n\nLOADING PAGE\n\n")
    else:  # request.method is POST - Someone clicked submit
        if form.validate_on_submit():
            print('-------------------------------')
            print(f"Username: {form.username.data}")
            print(f"Password: {form.password.data}")
            print('-------------------------------')
            title = f"Welcome! {form.username.data}"
        else:  # a validator failed... lets see which one(s)
            print('-------------------------------')
            print('ERROR:')
            print(form.errors)
            print('-------------------------------')
    return render_template('signup.html', form=form, title=title)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    title = "Dashboard"
    form = LoginForm()
    if request.method == "GET":
        print("\n\nLOADING PAGE\n\n")
    else:
        if form.validate_on_submit():
            print('-------------------------------')
            print(f"Username: {form.username.data}")
            print(f"Password: {form.password.data}")
            print('-------------------------------')
            title = f"{form.username.data}'s dashboard"
        else:
            print('-------------------------------')
            print('ERROR:')
            print(form.errors)
            print('-------------------------------')
    return render_template('dashboard.html', title=title, form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
