from config import app, api
from flask_restplus import Resource

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
