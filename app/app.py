import flask
from flask import request, jsonify
import json
import requests
#from gevent.pywsgi import WSGIServer

app = flask.Flask(__name__)
app.config["DEBUG"] = True

"""
Data Records Format:

{"records":[{"value":
{"PROFILEID":"c2309eec","LATITUDE":37.7877,"LONGITUDE":-
122.4205}},{"value":{"PROFILEID":"18f4ea86","LATITUDE":37.3903,"LONGITUDE":-
122.0643}},{"value":{"PROFILEID":"4ab5cbad","LATITUDE":37.3952,"LONGITUDE":-
122.0813}},{"value":{"PROFILEID":"8b6eae59","LATITUDE":37.3944,"LONGITUDE":-
122.0813}}]}

"""

@app.route('/',methods=['GET'])
def index():

    final={}
    x=requests.get("http://172.16.238.9:8083/connectors")
    y=list(x.json())
    for i in y:
        varivel=requests.get("http://172.16.238.9:8083/connectors/"+i)
        final[varivel.json()["name"]]=varivel.json()["config"]["http.api.url"]

    return jsonify(final) 
    

buffers={}    

@app.route('/api/v1/<string:connector>', methods=['POST'])
def sendMessages(connector):
    if connector in buffers:
        buffers[connector].append(request.json)
    else:
        buffers[connector]=[request.json]
    return "Data has been received."


@app.route('/api/v1/messages/<string:connector>', methods=['GET'])
def getmessages(connector):
    if connector in buffers:
        return jsonify(buffers[connector])
    return "{\"Erro\":\"Connector not yet found\"}"

app.run(host="0.0.0.0", port=5000)
#WSGIServer(('localhost', 5000), app).serve_forever() #To avoid Broken Pipe Errors