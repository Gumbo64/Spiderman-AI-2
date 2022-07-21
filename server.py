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
def my_view_func(allvar):
    vars = allvar.split("|")
    names = vars[::2]
    values = vars[1::2]
    valdict = {}
    for i in range(len(names)):
        valdict[names[i]] = float(values[i])
    window_vars[int(valdict["gameid"])] = valdict
    # system('clear')
    # for i in window_vars:
    #     print(i) 
       
    fire = window_cooldowns[int(valdict["gameid"])] > 15
    if fire:
        window_cooldowns[int(valdict["gameid"])] = 0
    else:
        window_cooldowns[int(valdict["gameid"])]+=1


    action = {'x': random()-0.5, 'y':random()-0.5,'fire':fire}
    response = urllib.parse.urlencode(action)
    return response

if __name__ == '__main__':
    my_os = platform.system()
    # config
    c = {
        "N_WINDOWS":50,
        "WIDTH":100,
        "HEIGHT":100,
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
    