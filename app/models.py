from app.routes import db


class Theme(db.Model):
    __tablename__ = "Theme"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    folios = db.relationship("Folio", backref="theme")
    arts = db.relationship("Art", backref="theme")

    def __repr__(self):
        return self.name


class Folio(db.Model):
    __tablename__ = "Folio"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('Theme.id'))

    artists = db.relationship('Artist', secondary=ArtistFolio, back_populates='folios')
    layouts = db.relationship('Layout', secondary=FolioLayout, back_populates='folios')
    arts = db.relationship('Art', secondary=ArtFolio, back_populates='folios')

    def __repr__(self):
        return f'Folio: {self.name}'


class Artist(db.Model):
    __tablename__ = "Artist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    photo = db.Column(db.Text)

    folios = db.relationship('Folio', secondary=ArtistFolio, back_populates='artists')
    arts = db.relationship("Art", backref="artist")

    def __repr__(self):
        return self.name


class Layout(db.Model):
    __tablename__ = "Layout"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    folios = db.relationship('Folio', secondary=FolioLayout, back_populates='layouts')

    def __repr__(self):
        return f'Layout {self.id}'


class Art(db.Model):
    __tablename__ = "Art"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    theme_id = db.Column(db.Integer, db.ForeignKey('Theme.id'))

    meanings = db.relationship('Meaning', secondary=ArtMeaning, back_populates='arts')
    folios = db.relationship('Folio', secondary=ArtFolio, back_populates='arts')

    def __repr__(self):
        return f'Art: {self.name}'


class Meaning(db.Model):
    __tablename__ = "Meaning"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    arts = db.relationship('Art', secondary=ArtMeaning, back_populates='meanings')

    def __repr__(self):
        return self.description
