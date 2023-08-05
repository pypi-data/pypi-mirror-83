from flask import Flask
from skywalking_flask import SkywalkingFlask

app = Flask(__name__)

SkywalkingFlask(app, service='My Service 2', collector='192.168.3.202:11800')


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1', debug=True)
