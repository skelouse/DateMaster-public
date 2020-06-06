# File: main_emulate.py
import flask

from main import skelouse

app = flask.Flask('functions')
methods = ['GET', 'POST', 'PUT', 'DELETE']

@app.route('/skelouse', methods=methods)
@app.route('/skelouse/<path>', methods=methods)
@app.route('/admin', methods=methods)
@app.route('/admin/<path>', methods=methods)
#@app.route('/skelouse/<path>/id')
def catch_all(path='x'):
    flask.request.path = '/' + path
    #return heroes(flask.request)
    return skelouse(flask.request)

if __name__ == '__main__':
    app.run()