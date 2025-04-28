from app import app
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy  # no more boring old SQL for us!
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "database.db")
db.init_app(app)


import app.models as models


# --- Routes ---

@app.route('/')
def root():
    return render_template('home.html', page_title='HOME')

@app.route('/about')
def about():
    return render_template('about.html', page_title='ABOUT')

@app.route('/themes')
def all_themes():
    themes = models.Theme.query.all()
    return render_template('themes.html', themes=themes)

@app.route('/folios')
def all_folios():
    folios = models.Folio.query.all()
    return render_template('folios.html', folios=folios)

@app.route('/artists')
def all_artists():
    artists = models.Artist.query.all()
    return render_template('artists.html', artists=artists)

@app.route('/artwork')
def all_arts():
    arts = models.Art.query.all()
    return render_template('artwork.html', arts=arts)

@app.route('/theme/<int:id>')
def theme(id):
    theme = models.Theme.query.get_or_404(id)
    return render_template('theme.html', theme=theme)

@app.route('/folio/<int:id>')
def folio(id):
    folio = models.Folio.query.get_or_404(id)
    return render_template('folio.html', folio=folio, artists=folio.artists, layouts=folio.layouts, arts=folio.arts)

@app.route('/artist/<int:id>')
def artist(id):
    artist = models.Artist.query.get_or_404(id)
    return render_template('artist.html', artist=artist)

@app.route('/art/<int:id>')
def art(id):
    art = models.Art.query.get_or_404(id)
    return render_template('art.html', art=art, meanings=art.meanings, folios=art.folios)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
