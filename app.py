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
            return {'success': True, 'playlists': {'playlist': playlists}}
        except Exception as e:
            print(e)
            return {'success': False, 'message': 'Failed to get playlists'}

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
                albums = db.Album.query.order_by(db.Album.title).offset(offset).limit(limit).all()
            elif request_type == 'alphabeticalByName':
                albums = db.Album.query.order_by(func.random()).offset(offset).limit(limit).all()
            else:
                return {'success': False, 'message': 'Wrong album type'}
            result = []
            for a in albums:
                result.append({
                    'id': a.id,
                    'name': a.title,
                    'artist': 'Rosé',
                    'artistId': '1',
                    'coverArt': a.cover_image,
                    'songCount': 6,
                    'duration': 1678,
                    'playCount': 1234,
                    'created': str(a.date_added),
                    'year': 2007,
                    'genre': a.genre.name
                })
            return {'success': True, 'albumList2': {'album': result}}
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

@ns_rest.route('/getArtists')
class getArtists(Resource):
    @jwt_required()
    def get(self):
        try:
            artists = db.get_all_artists()
            return {
                'success': True,
                'artists': {
                    'ignoredArticles': 'The El La Los Las Le',
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
        if request.args.get('albumId'):
            album_id = request.args.get('albumId')
            success = db.star_album(current_user, album_id) is not None
            return {'success': success}
        else:
            return {'success': False, 'message': 'Wrong starred type'}

@ns_rest.route('/unstar')
class unstar(Resource):
    @jwt_required()
    def get(self):
        if request.args.get('albumId'):
            album_id = request.args.get('albumId')
            success = db.unstar_album(current_user, album_id)
            return {'success': success}
        else:
            return {'success': False, 'message': 'Wrong unstarred type'}

@ns_rest.route('/getGenres')
class getGenres(Resource):
    @jwt_required()
    def get(self):
        return {    "success": True,    "genres": {      "genre": [        {          "songCount": 118,          "albumCount": 13,          "value": "(255)"        },        {          "songCount": 56,          "albumCount": 6,          "value": "Podcast"        },        {          "songCount": 1,          "albumCount": 1,          "value": "Ska"        }      ]    }  }

@ns_rest.route('/getStarred2')
class getStarred2(Resource):
    @jwt_required()
    def get(self):
        return {    "success": True,    "starred2": {      "song": [        {          "id": "358",          "parent": "346",          "isDir": false,          "title": "Drop that apple, bitch!",          "album": "Eve",          "artist": "Shearer",          "track": 8,          "year": 2008,          "genre": "Rock",          "coverArt": "346",          "size": 614528,          "contentType": "audio/mpeg",          "suffix": "mp3",          "duration": 37,          "bitRate": 128,          "path": "Shearer/Eve/08 - Drop that apple, bitch!.mp3",          "averageRating": 1,          "playCount": 747,          "created": "2017-03-12T11:05:16.000Z",          "starred": "2021-04-04T08:59:22.515Z",          "albumId": "37",          "artistId": "18",          "type": "music"        },        {          "id": "273",          "parent": "261",          "isDir": false,          "title": "Project Wildfire",          "album": "Robot Wars",          "artist": "Binärpilot",          "track": 4,          "year": 2007,          "genre": "Electronic",          "coverArt": "261",          "size": 5060736,          "contentType": "audio/mpeg",          "suffix": "mp3",          "duration": 316,          "bitRate": 128,          "path": "Binaerpilot/Robot Wars/04_binaerpilot_-_project_wildfire.mp3",          "averageRating": 5,          "playCount": 2734,          "created": "2017-03-12T11:08:03.000Z",          "starred": "2021-04-04T08:58:55.660Z",          "albumId": "29",          "artistId": "15",          "type": "music"        },        {          "id": "369",          "parent": "368",          "isDir": false,          "title": "Faya Ska",          "album": "Full Faya II",          "artist": "FUll Faya Orchestra",          "track": 2,          "year": 2008,          "genre": "Reggae",          "coverArt": "368",          "size": 4255872,          "contentType": "audio/mpeg",          "suffix": "mp3",          "duration": 264,          "bitRate": 128,          "path": "Full Faya Orchestra/Full Faya II/02 - Faya Ska.mp3",          "playCount": 1316,          "created": "2017-03-12T11:05:23.000Z",          "starred": "2018-09-25T06:54:12.810Z",          "albumId": "38",          "artistId": "19",          "type": "music"        }      ]    }  }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
