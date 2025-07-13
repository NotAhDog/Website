from app.routes import db

# Association Tables

Folio_Layout = db.Table(
    'Folio_Layout',
    db.Column('folio_id', db.Integer, db.ForeignKey('Folio.id'), primary_key=True),
    db.Column('layout_id', db.Integer, db.ForeignKey('Layout.id'), primary_key=True)
)

# Models


class Theme(db.Model):
    __tablename__ = "Theme"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    folios = db.relationship("Folio", backref="theme")

    def __repr__(self):
        return self.name


class Folio(db.Model):
    __tablename__ = "Folio"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('Theme.id'))

    layouts = db.relationship('Layout', secondary=Folio_Layout, back_populates='folios')

    def __repr__(self):
        return f'Folio: {self.name}'


class Layout(db.Model):
    __tablename__ = "Layout"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    folios = db.relationship('Folio', secondary=Folio_Layout, back_populates='layouts')

    def __repr__(self):
        return f'Layout {self.id}'


class Meaning(db.Model):
    __tablename__ = "Meaning"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.description


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'User {self.id}'


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    look = db.Column(db.String(150), nullable=False)
    addition = db.Column(db.String(150), nullable=False)
    easytouse = db.Column(db.String(150), nullable=False)
    other = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
