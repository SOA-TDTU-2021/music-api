from config import sql
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import math, random, uuid

class User(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    email = sql.Column(sql.String(120), unique=True)
    password_hash = sql.Column(sql.String(100))
    roles = sql.Column(sql.Integer)
    avatar_file = sql.Column(sql.String(100))
    date_created = sql.Column(sql.DateTime, default=datetime.now)
    otp_code = sql.Column(sql.String(10))
    otp_expiration_datetime = sql.Column(sql.DateTime, default=datetime(1970, 1, 1))
    created_artists = sql.relationship('Artist', backref=sql.backref('created_by', lazy=True))
    created_albumes = sql.relationship('Album', backref=sql.backref('created_by', lazy=True))
    created_playlists = sql.relationship('Playlist', backref=sql.backref('created_by', lazy=True))
    created_tracks = sql.relationship('Track', backref=sql.backref('created_by', lazy=True))
    rated_albums = sql.relationship('AlbumRating', backref=sql.backref('rated_by', lazy=True))
    rated_tracks = sql.relationship('TrackRating', backref=sql.backref('rated_by', lazy=True))
    rated_playlists = sql.relationship('PlaylistRating', backref=sql.backref('rated_by', lazy=True))
    played = sql.relationship('Played', backref=sql.backref('user', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_jwt(self):
        """
        Generates the Auth Token
        :return: string
        """
        return create_access_token(identity=self)

playlists_tracks = sql.Table('playlists_tracks',
    sql.Column('playlist_id', sql.Integer, sql.ForeignKey("playlist.id"), primary_key=True),
    sql.Column('track_id', sql.Integer, sql.ForeignKey("track.id"), primary_key=True)
)

albums_artists = sql.Table('albums_artists',
    sql.Column('album_id', sql.Integer, sql.ForeignKey("album.id"), primary_key=True),
    sql.Column('artist_id', sql.Integer, sql.ForeignKey("artist.id"), primary_key=True)
)

tracks_artists = sql.Table('tracks_artists',
    sql.Column('track_id', sql.Integer, sql.ForeignKey("track.id"), primary_key=True),
    sql.Column('artist_id', sql.Integer, sql.ForeignKey("artist.id"), primary_key=True)
)

class Artist(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    avatar_file = sql.Column(sql.String(100))
    country = sql.Column(sql.String(100))
    info = sql.Column(sql.Text)
    date_added = sql.Column(sql.DateTime, default=datetime.now)
    date_modified = sql.Column(sql.DateTime, default=datetime.now)
    added_by_user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"))

class Genre(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    albums = sql.relationship('Album', backref=sql.backref('genre', lazy=True))

class Track(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    duration = sql.Column(sql.Integer)
    date_added = sql.Column(sql.DateTime, default=datetime.now)
    date_modified = sql.Column(sql.DateTime, default=datetime.now)
    album_id = sql.Column(sql.Integer, sql.ForeignKey("album.id"))
    added_by_user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"))
    artists = sql.relationship('Artist', secondary=tracks_artists, lazy='subquery',
        backref=sql.backref('tracks', lazy=True))
    rated = sql.relationship('TrackRating', backref=sql.backref('track', lazy=True))
    played = sql.relationship('Played', backref=sql.backref('track', lazy=True))

class Album(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(100))
    cover_image = sql.Column(sql.String(100))
    date_release = sql.Column(sql.DateTime, default=datetime(1970, 1, 1))
    date_added = sql.Column(sql.DateTime, default=datetime.now)
    date_modified = sql.Column(sql.DateTime, default=datetime.now)
    genres_id = sql.Column(sql.Integer, sql.ForeignKey("genre.id"))
    added_by_user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"))
    tracks = sql.relationship('Track', backref=sql.backref('album', lazy=True))
    artists = sql.relationship('Artist', secondary=albums_artists, lazy='subquery',
        backref=sql.backref('albums', lazy=True))
    rated = sql.relationship('AlbumRating', backref=sql.backref('album', lazy=True))

class Playlist(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    image = sql.Column(sql.String(100))
    is_public = sql.Column(sql.Boolean)
    date_added = sql.Column(sql.DateTime, default=datetime.now)
    date_modified = sql.Column(sql.DateTime, default=datetime.now)
    added_by_user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"))
    tracks = sql.relationship('Track', secondary=playlists_tracks, lazy='subquery',
        backref=sql.backref('playlists', lazy=True))
    rated = sql.relationship('PlaylistRating', backref=sql.backref('playlist', lazy=True))

class AlbumRating(sql.Model):
    album_id = sql.Column(sql.Integer, sql.ForeignKey("album.id"), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"), primary_key=True)
    time = sql.Column(sql.DateTime, default=datetime.now)

class TrackRating(sql.Model):
    track_id = sql.Column(sql.Integer, sql.ForeignKey("track.id"), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"), primary_key=True)
    time = sql.Column(sql.DateTime, default=datetime.now)

class PlaylistRating(sql.Model):
    playlist_id = sql.Column(sql.Integer, sql.ForeignKey("playlist.id"), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"), primary_key=True)
    time = sql.Column(sql.DateTime, default=datetime.now)

class Played(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"))
    track_id = sql.Column(sql.Integer, sql.ForeignKey("track.id"))
    count = sql.Column(sql.Integer)
    last_play_time = sql.Column('time', sql.DateTime, default=datetime.now)

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).one_or_none()

def get_user_by_email(user_email):
    return User.query.filter_by(email=user_email).one_or_none()

def add_user(name, email, password):
    user = User(name=name, email=email)
    user.set_password(password)
    sql.session.add(user)
    try:
        sql.session.commit()
        return user.id
    except Exception as e:
        return None

def get_all_playlists():
    result = []
    playlists = Playlist.query.all()
    for p in playlists:
        result.append({
            'id': p.id,
            'name': p.name,
            'comment': '',
            'owner': p.created_by.name,
            'public': p.is_public,
            'songCount': 12,
            'duration': 2483,
            'created': str(p.date_added),
            'changed': str(p.date_modified),
            'coverArt': p.image
        })
    return result

def get_all_artists():
    artists = Artist.query.all()
    result = []
    indexes = {}
    for a in artists:
        first_char = a.name[0].upper()
        count = 0
        for album in a.albums:
            count += 1
        if first_char not in indexes.keys():
            indexes[first_char] = [{
                'id': a.id,
                'name': a.name,
                'coverArt': a.avatar_file,
                'artistImageUrl': 'https://lastfm-img2.akamaized.net/i/u/da0f3b84bd72470492de2a2dc58afbe2.png',
                'albumCount': count
            }]
        else:
            indexes[first_char].append({
                'id': a.id,
                'name': a.name,
                'coverArt': a.avatar_file,
                'artistImageUrl': 'https://lastfm-img2.akamaized.net/i/u/da0f3b84bd72470492de2a2dc58afbe2.png',
                'albumCount': count
            })
    for i in indexes.keys():
        result.append({
            'name': i,
            'artist': indexes[i]
        })
    return result

def get_album(user, album_id):
    album = Album.query.filter_by(id=album_id).one_or_none()
    songs = []
    for tr in album.tracks:
        songs.append({
            'id': tr.id,
            'parent': 261,
            'isDir': False,
            'title': tr.name,
            'album': album.title,
            'artist': 'Artist 1',
            'tracks': 1,
            'year': 2021,
            'genre': album.genre.name,
            'coverArt': album.cover_image,
            'size': 100000,
            'contentType': 'audio/mpeg',
            'suffix': 'mp3',
            'duration': 285,
            'bitRate': 128,
            'path': 'tracks/track1.mp3',
            'playCount': 1000,
            'created': str(tr.date_added),
            'starred': str(tr.date_added),
            'albumId': album.id,
            'artistId': '1',
            'type': 'music'
        })
    starred = AlbumRating.query.filter_by(album_id=album.id).filter_by(user_id=user.id).one_or_none()
    return {
        'id': album.id,
        'name': album.title,
        'artist': 'Artist 1',
        'artistId': '1',
        'coverArt': album.cover_image,
        'songCount': 2,
        'duration': 1234,
        'playCount': 100000,
        'created': str(album.date_added),
        'starred': starred is not None,
        'year': 2021,
        'genre': album.genre.name,
        'song': songs
    }

def star_album(user, album_id):
    star = AlbumRating(album_id=album_id)
    try:
        user.rated_albums.append(star)
        sql.session.add(user)
        sql.session.commit()
        return star.album_id
    except Exception as e:
        print(e)
        return None

def unstar_album(user, album_id):
    try:
        star = AlbumRating.query.filter_by(album_id=album_id).filter_by(user_id=user.id).one_or_none()
        sql.session.delete(star)
        sql.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
