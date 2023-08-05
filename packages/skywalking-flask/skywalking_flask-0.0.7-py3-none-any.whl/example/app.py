import requests
from flask import Flask

from skywalking_flask import SkywalkingFlask

app = Flask(__name__)
SkywalkingFlask(app, service='My Service 1', collector='192.168.3.202:11800')


@app.route('/')
def hello_world():
    r = requests.get("http://127.0.0.1:8081/hello")
    return r.text


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
