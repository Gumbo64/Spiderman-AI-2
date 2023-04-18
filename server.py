import flask
from flask import request
from subprocess import Popen
import platform
from os import system
import urllib
from random import random,getrandbits

import logging

app = flask.Flask(__name__)
logging.getLogger('werkzeug').disabled = True

window_vars = []
window_cooldowns = []

@app.route('/<allvar>', methods=['GET'])
def receiver(allvar):
    # parsing game state from URL
    vars = allvar.split("|")
    names = vars[:-2:2]
    values = vars[1:-2:2]
    raycasts = list(map(float,vars[-1].split(",")))
    valdict = {}

    action = {'x': random()-0.5, 'y':random()-0.5,'fire':True}
    # action = {'x': 0.5, 'y':-0.5,'fire':fire}
    # print(action)
    response = urllib.parse.urlencode(action)
    return response

if __name__ == '__main__':
    my_os = platform.system()
    # config
    c = {
        "N_WINDOWS":4,
        # "WIDTH":500,
        # "HEIGHT":363,
        "WIDTH":300,
        "HEIGHT":300,
    }

    if my_os == "Linux":
        for i in range(c["N_WINDOWS"]):
            window_vars.append({})
            window_cooldowns.append(0)
            Popen(['./ruffle', "spidermanmodded.swf","--width",str(c["WIDTH"]), "--height",str(c["HEIGHT"]), "-P","gameid="+str(i)])
    else:
        for i in range(c["N_WINDOWS"]):
            window_vars.append({})
            window_cooldowns.append(0)
            Popen(['./ruffle.exe', "spidermanmodded.swf","--width",str(c["WIDTH"]), "--height",str(c["HEIGHT"]), "-P","gameid="+str(i)])
    app.run(port=8000)
   

