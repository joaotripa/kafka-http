import flask
from flask import request
import json
#from gevent.pywsgi import WSGIServer

app = flask.Flask(__name__)
app.config["DEBUG"] = True

messages = []

@app.route('/api/v1/messages', methods=['POST'])
def sendMessages():

    dic = request.json
    messages.append(dic)
    # for value in dic['records']:
    #     data = value['value']
    #     print("PROFILEID: " + str(data['PROFILEID']) + " LATITUDE: " + str(data['LATITUDE']) + 
    #     " LONGITUDE: " + str(data['LONGITUDE']))

    return "Data has been received."    

@app.route('/api/v1/getmessages', methods=['GET'])
def getmessages():
    return str(messages)

app.run(host="0.0.0.0", port=5000)
#WSGIServer(('localhost', 5000), app).serve_forever() #To avoid Broken Pipe Errors