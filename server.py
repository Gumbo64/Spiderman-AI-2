import flask
from flask import request
from subprocess import Popen
from os import system


app = flask.Flask(__name__)
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
    system('clear')
    for i in window_vars:
        print(i) 
    return "swag"

if __name__ == '__main__':
    N_WINDOWS = 4
    for i in range(N_WINDOWS):
        print(i)
        window_vars.append({})
        Popen(['./ruffle', "spidermanmodded.swf","--width","1", "--height","1", "-P","gameid="+str(i)])
 
    app.run(port=8000)
    