


if __name__ == '__main__':
    while True:
        data = conn.recv(1024)
        if not data:
            continue


        vars = parse_vars(data)
        

        print(vars)
        # print([vars["w1x"],vars["w1y"],vars["w1vx"],vars["w1vy"],vars["w2x"],vars["w2y"],vars["w2vx"],vars["w2vy"]])
        action = {'x': random()-0.5, 'y':random()-0.5,'fire':True}






        encoded_action = urllib.parse.urlencode(action)
        response = "HTTP/1.1 " + str(Response(text=encoded_action))
        conn.send(response.encode('utf-8'))
        # time.sleep(1)
        # print("FPS: ", 1.0 / max(time.time() - start_time,1e-10))
        start_time = time.time()
    sock.close()
