from config import app

@app.route('/ping')
def hello_world():
    return 'pong!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
