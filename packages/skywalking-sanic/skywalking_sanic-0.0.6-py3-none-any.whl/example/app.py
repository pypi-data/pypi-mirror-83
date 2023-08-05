import requests
from sanic import Sanic
from sanic.response import text

from skywalking_sanic import SkywalkingSanic

app = Sanic(__name__)


@app.route('/')
def hello_world(request):
    r = requests.get('http://127.0.0.1:8081/hello')
    return text(r.text)


SkywalkingSanic(app, service='My Service 1', collector='192.168.3.202:11800')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
