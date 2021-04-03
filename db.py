from config import sql
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

albums_artists = sql.Table('albums_artists',
    sql.Column('album_id', sql.Integer, sql.ForeignKey("album.id"), primary_key=True),
    sql.Column('artist_id', sql.Integer, sql.ForeignKey("artist.id"), primary_key=True)
)

playlists_tracks = sql.Table('playlists_tracks',
    sql.Column('playlist_id', sql.Integer, sql.ForeignKey("playlist.id"), primary_key=True),
    sql.Column('track_id', sql.Integer, sql.ForeignKey("track.id"), primary_key=True)
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
    albums = sql.relationship('Album', secondary=albums_artists, lazy='subquery',
        backref=sql.backref('artists', lazy=True))
    tracks = sql.relationship('Track', secondary=tracks_artists, lazy='subquery',
        backref=sql.backref('artists', lazy=True))

class Genre(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    albums = sql.relationship('Album', backref=sql.backref('genre', lazy=True))

class Track(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    duration = sql.Column(sql.Float)
    date_added = sql.Column(sql.DateTime, default=datetime.now)
    date_modified = sql.Column(sql.DateTime, default=datetime.now)
    added_by_user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"))
    rated = sql.relationship('TrackRating', backref=sql.backref('track', lazy=True))

class Album(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(100))
    cover_image = sql.Column(sql.String(100))
    date_release = sql.Column(sql.DateTime, default=datetime(1970, 1, 1))
    date_added = sql.Column(sql.DateTime, default=datetime.now)
    date_modified = sql.Column(sql.DateTime, default=datetime.now)
    genres_id = sql.Column(sql.Integer, sql.ForeignKey("genre.id"))
    added_by_user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"))
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
    star = sql.Column(sql.Integer)
    time = sql.Column(sql.DateTime, default=datetime.now)

class TrackRating(sql.Model):
    track_id = sql.Column(sql.Integer, sql.ForeignKey("track.id"), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"), primary_key=True)
    star = sql.Column(sql.Integer)
    time = sql.Column(sql.DateTime, default=datetime.now)

class PlaylistRating(sql.Model):
    playlist_id = sql.Column(sql.Integer, sql.ForeignKey("playlist.id"), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"), primary_key=True)
    star = sql.Column(sql.Integer)
    time = sql.Column(sql.DateTime, default=datetime.now)

class PlayCount(sql.Model):
    track_id = sql.Column(sql.Integer, sql.ForeignKey("track.id"), primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("user.id"), primary_key=True)
    count = sql.Column(sql.Integer)