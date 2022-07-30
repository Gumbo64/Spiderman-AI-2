import socket
import time
import urllib.parse
from random import random
from subprocess import Popen
import platform
from collections import defaultdict
from webob import Response
import selectors

window_vars = {}
window_cooldowns = defaultdict(lambda: 0)

def parse_vars(data):
    str_data = data.decode("utf-8", "ignore")
    str_data = str_data[(str_data.find("/") + 1):(str_data.find(" HTTP"))]
    vars = str_data.split("|")
    names = vars[:-2:2]
    values = vars[1:-2:2]
    raycasts = list(map(float,vars[-1].split(",")))

    valdict = {"raycasts":raycasts}
    for i in range(len(names)):
        valdict[names[i]] = float(values[i])

    win_index =  int(valdict["gameid"])
    window_vars[win_index] = valdict
    return valdict

def get_fire(win_index):
    fire = window_cooldowns[win_index] > 15
    if fire:
        window_cooldowns[win_index] = 0
    else:
        window_cooldowns[win_index]+=1
    return fire
    

def open_windows():
    ruffle_launchers = {
        "Linux":"./ruffle",
        "Windows":"./ruffle.exe"
    }

    my_os = platform.system()
    

    # for i in range(c["N_WINDOWS"]):
    return Popen([ruffle_launchers[my_os], "spidermanmodded.swf","--width",str(c["WIDTH"]), "--height",str(c["HEIGHT"]),"-g","dx12","-P","gameid="+str(0)])




c = {
    # "N_WINDOWS":10,
    # "WIDTH":500,
    # "HEIGHT":363,
    "WIDTH":300,
    "HEIGHT":300,
}


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8000))

p = open_windows()

sock.listen()
sock.setblocking(False)
sock.settimeout(None)
conn, addr = sock.accept()


start_time = time.time()



if __name__ == '__main__':
    while True:
        data = conn.recv(1024)
        if not data:
            continue


        vars = parse_vars(data)
        

        print(vars)
        # print([vars["w1x"],vars["w1y"],vars["w1vx"],vars["w1vy"],vars["w2x"],vars["w2y"],vars["w2vx"],vars["w2vy"]])
        action = {'x': random()-0.5, 'y':random()-0.5,'fire':get_fire(vars["gameid"])}






        encoded_action = urllib.parse.urlencode(action)
        response = "HTTP/1.1 " + str(Response(text=encoded_action))
        conn.send(response.encode('utf-8'))
        # time.sleep(1)
        # print("FPS: ", 1.0 / max(time.time() - start_time,1e-10))
        start_time = time.time()
    sock.close()
