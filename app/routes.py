from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from .forms import LoginForm, SignupForm, FeedbackForm
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "database.db")
db.init_app(app)


import app.models as models
from app.models import User, Feedback
app.secret_key = 'CorrectHorseBatteryStaple'


def GetLogin():
    username = session.get('username')
    if username:
        return True
    return False


# --- Routes ---


@app.route('/', methods=['GET', 'POST'])  # Home page
def root():
    print(request.args.get('user'))
    return render_template('home.html', page_title='HOME', login=GetLogin())


@app.route('/about')  # About page
def about():
    title = "About"
    return render_template('about.html', page_title='ABOUT', title=title, login=GetLogin())


@app.route('/folios')  # Folios page
def all_folios():
    title = "Folios"
    folios = models.Folio.query.all()
    return render_template('folios.html', folios=folios, title=title, folio_num=len(folios), login=GetLogin())


@app.route('/projects')  # projects page
def all_artists():
    title = "Projects"
    return render_template('projects.html',  title=title, login=GetLogin())


@app.route('/folios/<int:id>')
def folio(id):
    folio = models.Folio.query.options(
        db.joinedload(models.Folio.theme),
        db.joinedload(models.Folio.layouts)
    ).get_or_404(id)
    return render_template('detailfolios.html', folio=folio, login=GetLogin())


@app.route('/artist/<int:id>')
def artist(id):
    artist = models.Artist.query.get_or_404(id)
    return render_template('artist.html', artist=artist, login=GetLogin())


@app.route('/art/<int:id>')
def art(id):
    title = "Art - <int:id>"
    art = models.Art.query.get_or_404(id)
    return render_template('art.html', art=art, meanings=art.meanings, folios=art.folios, title=title, login=GetLogin())


@app.route('/secret')  # Secret page
def secret():
    title = "Secret"
    return render_template('secret.html', title=title, login=GetLogin())


@app.route('/account', methods=['GET', 'POST'])  # Login page
def login():
    error = False
    title = "Login"
    form = LoginForm()
    if request.method == "GET":
        print("\n\nLOADING PAGE\n\n")
    else:  # request.method is POST - Someone clicked submit
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            print('-------------------------------')
            print(f"Username: {form.username.data}")
            print(f"Password: {form.password.data}")
            print('-------------------------------')
        else:  # a validator failed... lets see which one(s)
            print('-------------------------------')
            print('ERROR:')
            print(form.errors)
            print('-------------------------------')

        account = User.query.filter_by(username=username).first()

        if account and check_password_hash(account.password, password):
            session['username'] = username
            return redirect(url_for('dashboard'))  # or wherever
        else:
            error = True
            flash("Invalid username or password", "danger")

    return render_template('login.html', form=form, title=title, login=GetLogin(), error=error)


@app.route('/signup', methods=['GET', 'POST'])  # Signup page
def signup():
    errors = []
    title = "Signup"
    form = SignupForm()
    if request.method == "GET":
        print("\n\nLOADING PAGE\n\n")
    else:  # request.method is POST - Someone clicked submit
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            print('-------------------------------')
            print(f"Username: {form.username.data}")
            print(f"Password: {form.password.data}")
            print('-------------------------------')
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                errors.append("Username already exists")
                flash("Username already taken. Try another one.", "danger")
            else:
                # Hash the password before saving
                hashed_password = generate_password_hash(password)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created successfully!", "success")
                return redirect(url_for('login'))  # Redirect to login page
        else:  # a validator failed... lets see which one(s)
            print('-------------------------------')
            print('ERROR:')
            print(form.errors)
            print('-------------------------------')

        # Check if user already exists

    return render_template('signup.html', form=form, title=title, login=GetLogin(), errors=errors)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_id = models.User.query.filter_by(username=session.get('username')).first().id
    print(user_id, "uid")
    submittedforms = Feedback.query.filter_by(user_id=user_id).all()
    title = "Dashboard"
    form = FeedbackForm()
    if request.method == "GET":
        print("\n\nLOADING PAGE\n\n")
    else:
        try:
            id_to_delete = request.form['delete_id']
            form_to_delete = Feedback.query.filter_by(id=id_to_delete).first()
            db.session.delete(form_to_delete)
            db.session.commit()
        except:
            if form.validate_on_submit():
                    looks = form.look.data
                    additions = form.additions.data
                    easytouse = form.easytouse.data
                    other = form.other.data
                    print('-------------------------------')
                    print(f"Looks: {form.look.data}")
                    print(f"Additions: {form.additions.data}")
                    print(f"Easy to use: {form.easytouse.data}")
                    print(f"Other feedback: {form.other.data}")
                    print('-------------------------------')
                    newform = Feedback(look=looks, addition=additions,
                                    easytouse=easytouse, other=other,
                                    user_id=user_id)
                    makeForm = True
                    for form_ in submittedforms:
                        if form_ == newform:
                            makeForm = False

                    if makeForm:
                        db.session.add(newform)
                        db.session.commit()
                        flash("Form Submitted!", "success")
            else:
                print('-------------------------------')
                print('ERROR:')
                print(form.errors)
                print('-------------------------------')
        

        submittedforms = Feedback.query.filter_by(user_id=user_id).all()


    return render_template('dashboard.html', title=title, form=form, login=GetLogin(),
                           submittedforms=submittedforms)

@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = None
    return redirect(url_for('root'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
