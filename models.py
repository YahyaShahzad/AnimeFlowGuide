from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))  # path relative to static/ (e.g., images/slug.jpg) -- optional
    episodes = db.Column(db.Integer)
    genres = db.Column(db.String(300))  # comma-separated list

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'))
    episode_no = db.Column(db.Integer)
    title = db.Column(db.String(200))
    type = db.Column(db.String(20))  # canon, filler, mixed
