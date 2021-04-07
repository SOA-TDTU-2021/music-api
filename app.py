from config import app, api, jwt, ns_rest
import db
from flask import request, send_file, safe_join, jsonify
from flask_restplus import Resource, fields
from flask_jwt_extended import current_user, jwt_required, set_access_cookies, unset_jwt_cookies
from sqlalchemy import asc, desc
from sqlalchemy.sql.expression import func

@jwt.user_identity_loader
def student_identity_lookup(user):
    return user.email

@jwt.user_lookup_loader
def student_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.get_user_by_email(identity)

@ns_rest.route('/login')
class UserLogin(Resource):
    @api.expect(api.model('Login model',
        {'email': fields.String(required = True),
            'password': fields.String(required = True)}))
    def post(self):
        data = request.get_json()
        user = db.get_user_by_email(data['email'])
        if user.check_password(data['password']):
            return {'success': True, 'message': 'Đăng nhập thành công', 'access_token':  user.generate_jwt()}
        else:
            api.abort(403, 'Sai tên đang nhập hoặc mật khẩu', success=False)

@ns_rest.route('/register')
class UserRegister(Resource):
    @api.expect(api.model('Register model',
        {'name': fields.String(required = True),
            'email': fields.String(required = True),
            'password': fields.String(required = True)}))
    def post(self):
        data = request.get_json()
        is_success = db.add_user(name=data['name'], email=data['email'], password=data['password']) is not None
        return {'success': is_success}

@ns_rest.route('/getPlaylists')
class GetPlaylists(Resource):
    @jwt_required()
    def get(self):
        try:
            playlists = db.get_all_playlists()
            return {'success': True, 'playlists': playlists}
        except Exception as e:
            print(e)
            return {'success': False, 'message': 'Failed to get playlists'}

@ns_rest.route('/getPlaylist')
class GetPlaylist(Resource):
    @jwt_required()
    def get(self):
        playlist_id = request.args.get('id')
        return {'success': True, 'playlist': db.get_playlist(playlist_id)}

@ns_rest.route('/createPlaylist')
class createPlaylist(Resource):
    @jwt_required()
    def get(self):
        playlist_name = request.args.get('name')
        result = db.create_playlist(playlist_name)
        if result is not None:
            return {'success': True, 'playlist': {
                'id': result.id,
                'name': result.name,
                'public': result.is_public
            }}

@ns_rest.route('/getAlbumList')
class getAlbumList(Resource):
    @jwt_required()
    def get(self):
        request_type = request.args.get('type')
        size = request.args.get('size')
        offset = request.args.get('offset')
        limit = offset + size
        try:
            if request_type == 'random':
                albums = db.Album.query.order_by(func.random()).offset(offset).limit(limit).all()
            elif request_type == 'recent':
                albums = []
                played = db.Played.query.filter_by(user_id=current_user.id).order_by(desc(db.Played.last_play_time)).offset(offset).limit(limit).all()
                for p in played:
                    if p.track.album in albums:
                        continue
                    albums.append(p.track.album)
            elif request_type == 'frequent':
                albums = []
                played = db.Played.query.filter_by(user_id=current_user.id).order_by(db.Played.count).offset(offset).limit(limit).all()
                for p in played:
                    if p.track.album in albums:
                        continue
                    albums.append(p.track.album)
            elif request_type == 'newest':
                albums = db.Album.query.order_by(desc(db.Album.id)).offset(offset).limit(limit).all()
            elif request_type == 'alphabeticalByName':
                albums = db.Album.query.order_by(db.Album.title).offset(offset).limit(limit).all()
            elif request_type == 'byGenre':
                albums = db.Album.query.join(db.Genre).filter_by(name=request.args.get('genre')).offset(offset).limit(limit).all()
            else:
                return {'success': False, 'message': 'Wrong album type'}
            result = []
            for a in albums:
                duration = 0
                for track in a.tracks:
                    duration += track.duration
                result.append({
                    'id': a.id,
                    'name': a.title,
                    'artist': a.artists[0].name,
                    'artistId': a.artists[0].id,
                    'coverArt': a.cover_image,
                    'songCount': len(a.tracks),
                    'duration': duration,
                    'created': str(a.date_added),
                    'year': a.year_release,
                    'genre': a.genre.name
                })
            return {'success': True, 'albums': result}
        except Exception as e:
            print(e)
            return {'success': False, 'message': 'Failed to get playlists'}

@ns_rest.route('/getAlbum')
class getAlbumList(Resource):
    @jwt_required()
    def get(self):
        album_id = request.args.get('id')
        return {'success': True, 'album': db.get_album(current_user, album_id)}

@ns_rest.route('/getCoverArt')
@api.representation('image/jpeg')
class getCoverArt(Resource):
    def get(self):
        filepath = safe_join("./", "rosé.jpg")
        return send_file(
            filename_or_fp=filepath,
            mimetype="image/jpeg"
        )

@ns_rest.route('/stream')
@api.representation('audio/mpeg')
class stream(Resource):
    def get(self):
        track_id = request.args.get('id')
        filepath = safe_join("./", "test.mp3")
        return send_file(
            filename_or_fp=filepath,
            mimetype="audio/mpeg"
        )

@ns_rest.route('/download')
@api.representation('application/x-download')
class stream(Resource):
    def get(self):
        track_id = request.args.get('id')
        filepath = safe_join("./", "test.mp3")
        return send_file(
            filename_or_fp=filepath,
            mimetype="application/x-download"
        )

@ns_rest.route('/getArtists')
class getArtists(Resource):
    @jwt_required()
    def get(self):
        try:
            artists = db.get_all_artists()
            return {
                'success': True,
                'artists': {
                    'index': artists
                }
            }
        except Exception as e:
            print(e)
            return {'success': False, 'message': 'Failed to get artists'}

@ns_rest.route('/getArtist')
class getArtist(Resource):
    @jwt_required()
    def get(self):
        artist_id = request.args.get('id')
        return {'success': True, 'artist': db.get_artist(artist_id)}

@ns_rest.route('/star')
class star(Resource):
    @jwt_required()
    def get(self):
        if request.args.get('id'):
            track_id = request.args.get('id')
            success = db.star_track(current_user, track_id) is not None
            return {'success': success}
        elif request.args.get('albumId'):
            album_id = request.args.get('albumId')
            success = db.star_album(current_user, album_id) is not None
            return {'success': success}
        else:
            return {'success': False, 'message': 'Wrong starred type'}

@ns_rest.route('/unstar')
class unstar(Resource):
    @jwt_required()
    def get(self):
        if request.args.get('id'):
            track_id = request.args.get('id')
            success = db.unstar_track(current_user, track_id)
            return {'success': success}
        elif request.args.get('albumId'):
            album_id = request.args.get('albumId')
            success = db.unstar_album(current_user, album_id)
            return {'success': success}
        else:
            return {'success': False, 'message': 'Wrong unstarred type'}

@ns_rest.route('/getGenres')
class getGenres(Resource):
    @jwt_required()
    def get(self):
        return {'success': True, 'genres': db.get_genres()}

@ns_rest.route('/getSongsByGenre')
class getSongsByGenre(Resource):
    @jwt_required()
    def get(self):
        offset = request.args.get('offset')
        count = request.args.get('count')
        result = []
        tracks = db.Track.query.filter_by(genre_name=request.args.get('genre')).offset(offset).limit(count).all()
        for track in tracks:
            starred_tracks = db.TrackRating.query.filter_by(track_id=track.id).filter_by(user_id=current_user.id).one_or_none()
            result.append({
                'id': track.id,
                'title': track.name,
                'album': track.album.title,
                'artist': track.artists[0].name,
                'duration': track.duration,
                'albumId': track.album.id,
                'artistId': track.artists[0].id,
                'starred': starred_tracks is not None
            })
        return {'success': True, 'songs':result}

@ns_rest.route('/getRandomSongs')
class getRandomSongs(Resource):
    @jwt_required()
    def get(self):
        size = request.args.get('size')
        result = []
        tracks = db.Track.query.order_by(func.random()).limit(size).all()
        for track in tracks:
            starred_tracks = db.TrackRating.query.filter_by(track_id=track.id).filter_by(user_id=current_user.id).one_or_none()
            result.append({
                'id': track.id,
                'title': track.name,
                'album': track.album.title,
                'artist': track.artists[0].name,
                'duration': track.duration,
                'albumId': track.album.id,
                'artistId': track.artists[0].id,
                'starred': starred_tracks is not None
            })
        return {'success': True, 'randomSongs': result}

@ns_rest.route('/getStarred')
class getStarred(Resource):
    @jwt_required()
    def get(self):
        result = []
        track_rating = db.TrackRating.query.filter_by(user_id=current_user.id).all()
        for r in track_rating:
            track = r.track
            starred_tracks = db.TrackRating.query.filter_by(track_id=track.id).filter_by(user_id=current_user.id).one_or_none()
            result.append({
                'id': track.id,
                'title': track.name,
                'album': track.album.title,
                'artist': track.artists[0].name,
                'duration': track.duration,
                'albumId': track.album.id,
                'artistId': track.artists[0].id,
                'starred': starred_tracks is not None
            })
        return {'success': True, 'starred': {'song': result, 'artist': None, 'album': None}}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
