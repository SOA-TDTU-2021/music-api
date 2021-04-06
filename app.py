from config import app, api, jwt, ns_rest
import db
from flask import request, send_file, safe_join, jsonify
from flask_restplus import Resource, fields
from flask_jwt_extended import current_user, jwt_required, set_access_cookies, unset_jwt_cookies

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
    def get(self):
        return {   "subsonic-response" : {      "status" : "ok",      "version" : "1.16.1",      "playlists" : {         "playlist" : [ {            "id" : "1144",            "name" : "2020-06-05. new",            "comment" : "",            "owner" : "guest4",            "public" : True,            "songCount" : 12,            "duration" : 2483,            "created" : "2020-08-23T15:05:42.579Z",            "changed" : "2021-04-04T08:25:29.823Z",            "coverArt" : "pl-1144"         }, {            "id" : "453",            "name" : "Apr 24, 2018 5:01 PM",            "owner" : "guest4",            "public" : False,            "songCount" : 22,            "duration" : 5555,            "created" : "2018-04-24T17:01:16.839Z",            "changed" : "2020-11-25T18:38:50.686Z",            "coverArt" : "pl-453"         } ]      }   }}

@ns_rest.route('/getAlbumList2')
class GetPlaylists(Resource):
    def get(self):
        return {   "subsonic-response" : {      "status" : "ok",      "version" : "1.16.1",      "albumList2" : {         "album" : [ {            "id" : "29",            "name" : "Robot Wars",            "artist" : "Binärpilot",            "artistId" : "15",            "coverArt" : "al-29",            "songCount" : 6,            "duration" : 1678,            "playCount" : 21240,            "created" : "2017-03-12T11:08:04.000Z",            "year" : 2007,            "genre" : "Electronic"         }, {            "id" : "28",            "name" : "Defrag",            "artist" : "Binärpilot",            "artistId" : "15",            "coverArt" : "al-28",            "songCount" : 4,            "duration" : 916,            "playCount" : 13701,            "created" : "2017-03-12T11:08:01.000Z",            "year" : 2005,            "genre" : "Electronic"         } ]      }   }}

@ns_rest.route('/getCoverArt')
@api.representation('image/jpeg')
class GetPlaylists(Resource):
    def get(self):
        filepath = safe_join("./", "rosé.jpg")
        return send_file(
            filename_or_fp=filepath,
            mimetype="image/jpeg"
        )

@ns_rest.route('/getArtists')
class GetPlaylists(Resource):
    def get(self):
        return {  "subsonic-response": {    "status": "ok",    "version": "1.16.1",    "artists": {      "ignoredArticles": "The El La Los Las Le",      "index": [        {          "name": "S",          "artist": [            {              "id": "18",              "name": "Shearer",              "coverArt": "ar-18",              "artistImageUrl": "https://lastfm-img2.akamaized.net/i/u/a7994c768b914543a2f2928d42559311.png",              "albumCount": 2            },            {              "id": "3",              "name": "Silence is Sexy",              "coverArt": "ar-3",              "artistImageUrl": "https://lastfm-img2.akamaized.net/i/u/959cdf5d084e4d42864a919281b3d58e.png",              "albumCount": 2            }          ]        },        {          "name": "U",          "artist": [            {              "id": "13",              "name": "Ugress",              "coverArt": "ar-13",              "artistImageUrl": "https://lastfm-img2.akamaized.net/i/u/6f2ce47efe15482eb5a3592e4d193ce7.png",              "albumCount": 4            }          ]        }      ]    }  }}

@ns_rest.route('/getGenres')
class GetPlaylists(Resource):
    def get(self):
        return {  "subsonic-response": {    "status": "ok",    "version": "1.16.1",    "genres": {      "genre": [        {          "songCount": 118,          "albumCount": 13,          "value": "(255)"        },        {          "songCount": 56,          "albumCount": 6,          "value": "Podcast"        },        {          "songCount": 1,          "albumCount": 1,          "value": "Ska"        }      ]    }  }}

@ns_rest.route('/getStarred2')
class GetPlaylists(Resource):
    def get(self):
        return {  "subsonic-response": {    "status": "ok",    "version": "1.16.1",    "starred2": {      "song": [        {          "id": "358",          "parent": "346",          "isDir": false,          "title": "Drop that apple, bitch!",          "album": "Eve",          "artist": "Shearer",          "track": 8,          "year": 2008,          "genre": "Rock",          "coverArt": "346",          "size": 614528,          "contentType": "audio/mpeg",          "suffix": "mp3",          "duration": 37,          "bitRate": 128,          "path": "Shearer/Eve/08 - Drop that apple, bitch!.mp3",          "averageRating": 1,          "playCount": 747,          "created": "2017-03-12T11:05:16.000Z",          "starred": "2021-04-04T08:59:22.515Z",          "albumId": "37",          "artistId": "18",          "type": "music"        },        {          "id": "273",          "parent": "261",          "isDir": false,          "title": "Project Wildfire",          "album": "Robot Wars",          "artist": "Binärpilot",          "track": 4,          "year": 2007,          "genre": "Electronic",          "coverArt": "261",          "size": 5060736,          "contentType": "audio/mpeg",          "suffix": "mp3",          "duration": 316,          "bitRate": 128,          "path": "Binaerpilot/Robot Wars/04_binaerpilot_-_project_wildfire.mp3",          "averageRating": 5,          "playCount": 2734,          "created": "2017-03-12T11:08:03.000Z",          "starred": "2021-04-04T08:58:55.660Z",          "albumId": "29",          "artistId": "15",          "type": "music"        },        {          "id": "369",          "parent": "368",          "isDir": false,          "title": "Faya Ska",          "album": "Full Faya II",          "artist": "FUll Faya Orchestra",          "track": 2,          "year": 2008,          "genre": "Reggae",          "coverArt": "368",          "size": 4255872,          "contentType": "audio/mpeg",          "suffix": "mp3",          "duration": 264,          "bitRate": 128,          "path": "Full Faya Orchestra/Full Faya II/02 - Faya Ska.mp3",          "playCount": 1316,          "created": "2017-03-12T11:05:23.000Z",          "starred": "2018-09-25T06:54:12.810Z",          "albumId": "38",          "artistId": "19",          "type": "music"        }      ]    }  }}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
