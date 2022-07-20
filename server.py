import flask
from flask import request
app = flask.Flask(__name__)
 

@app.route('/<allvar>', methods=['GET'])
def my_view_func(allvar):
    vars = allvar.split("|")
    names = vars[::2]
    values = vars[1::2]
    valdict = {}
    for i in range(len(names)):
        valdict[names[i]] = float(values[i])

    print(valdict) 
    return "swag"

if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(port=8000)