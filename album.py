import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class AlreadyExists(Exception):
	pass

class Album(Base):
	__tablename__ = "album"

	id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
	year = sa.Column(sa.Integer)
	artist = sa.Column(sa.Text)
	genre = sa.Column(sa.Text)
	album = sa.Column(sa.Text)


def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)

	return session()


def find_artist(artist):
	session = connect_db()

	albums = session.query(Album).filter(Album.artist == artist).all()
	return albums


def save_album(year, artist, genre, album):
	assert isinstance(year, int), "Incorrect date"
	assert isinstance(artist, str), "Incorrect artist"
	assert isinstance(genre, str), "Incorrect genre"
	assert isinstance(album, str), "Incorrect album"

	session = connect_db()

	checked_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
	if checked_album is not None:
		raise AlreadyExists(f"Такой альбом уже записан, id - {checked_album.id}")

	new_album = Album(
    	year=year,
    	artist=artist,
    	genre=genre,
    	album=album
    )    

	session.add(new_album)
	session.commit()

	return new_album