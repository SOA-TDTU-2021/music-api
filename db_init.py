from config import sql
import db

# sql.create_all()

user = db.User(name='Sang', email='xsang.bui@gmail.com')
user.set_password('1234')
user2 = db.User(name='User 2', email='u2@gmail.com')
user2.set_password('1234')
playlist = db.Playlist(name='Playlist 1', image='pl1.jpg', is_public=True, added_by_user_id=1)
playlist2 = db.Playlist(name='Playlist 2', image='pl2.jpg', is_public=True, added_by_user_id=1)

# sql.session.add(user)
# sql.session.add(user2)
# sql.session.add(playlist)
sql.session.add(playlist2)
sql.session.commit()
