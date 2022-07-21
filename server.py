import flask
from flask import request
from subprocess import Popen
import platform
from os import system
import urllib

import logging

app = flask.Flask(__name__)
logging.getLogger('werkzeug').disabled = True

window_vars = []

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
    action = {'x': 200, 'y':30,'fire':True}
    response = urllib.parse.urlencode(action)
    return response

if __name__ == '__main__':
    my_os = platform.system()
    # config
    c = {
        "N_WINDOWS":4,
        "WIDTH":100,
        "HEIGHT":100,
    }

    if my_os == "Linux":
        for i in range(c["N_WINDOWS"]):
            window_vars.append({})
            Popen(['./ruffle', "spidermanmodded.swf","--width",str(c["WIDTH"]), "--height",str(c["HEIGHT"]), "-P","gameid="+str(i)])
    else:
        for i in range(c["N_WINDOWS"]):
            window_vars.append({})
            Popen(['./ruffle.exe', "spidermanmodded.swf","--width",str(c["WIDTH"]), "--height",str(c["HEIGHT"]), "-P","gameid="+str(i)])
    app.run(port=8000)
    