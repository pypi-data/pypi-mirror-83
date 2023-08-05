from sanic import Sanic
from sanic.response import json
from skywalking_sanic import SkywalkingSanic

app = Sanic(__name__)

SkywalkingSanic(app, service='My Service 2', collector='192.168.3.202:11800')


@app.route("/hello")
async def test(request):
    return json({"hello": "world"})


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1', debug=True)
