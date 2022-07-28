
# environment
import numpy as np
from matplotlib import pyplot as plt
from gym import Env
from gym.spaces import Box

import socket
import urllib.parse
from random import random
from subprocess import Popen
import platform
from webob import Response





class Spiderman_ENV(Env):
	def __init__(self):
		super().__init__()
		# Setup spaces
		
		self.input_dims = 32
		self.observation_space = Box(low=0, high=1, shape=(self.input_dims,), dtype=np.float64)

		# first 2 inputs effectively a normalised vector output
		# when u click in the game it calculates the angle and nothing else so this range is all you need
		# 3rd input is whether the agent wants to fire a web or not, if it the value is above a threshold it will fire
		# this is important because spamming shots causes the tip of the webs to fly away, meaning they won't attach to anything and spiderman dies

		self.action_space = Box( np.array([-1,-1,-1]), np.array([+1,+1,+1]))
			
		self.c = {
			# "N_WINDOWS":10,
			# "WIDTH":500,
			# "HEIGHT":363,
			"WIDTH":300,
			"HEIGHT":300,
			"COOLDOWN":10,
		}


		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(("localhost", 8000))

		self.open_windows()

		sock.listen()
		sock.setblocking(False)
		sock.settimeout(None)
		self.conn, addr = sock.accept()
		self.fire_cooldown = 0
	def open_windows(self):
		ruffle_launchers = {
			"Linux":"./ruffle",
			"Windows":"./ruffle.exe"
		}

		my_os = platform.system()
		

		# for i in range(c["N_WINDOWS"]):
		Popen([ruffle_launchers[my_os], "spidermanmodded.swf","--width",str(self.c["WIDTH"]), "--height",str(self.c["HEIGHT"]), "-P","gameid="+str(0)])


	def step(self, action_array):
		data = self.conn.recv(1024)
		self.vars = self.parse_vars(data)

		fire = (action_array[2] > 0) and self.fire_count > self.c["COOLDOWN"]
		if fire:
			self.fire_count = 0
		else:
			self.fire_count += 1
		action = {'x': action_array[0], 'y':action_array[1],'fire':fire}
		

		encoded_action = urllib.parse.urlencode(action)
		response = "HTTP/1.1 " + str(Response(text=encoded_action))
		self.conn.send(response.encode('utf-8'))


		observation = self.get_observation()
		done = self.get_done()
		reward = self.get_reward()
		
		
		
		# print(reward)
		info = {}
		return observation, reward, done, info


	def parse_vars(self,data):
		str_data = data.decode("utf-8", "ignore")
		str_data = str_data[(str_data.find("/") + 1):(str_data.find(" HTTP"))]
		vars = str_data.split("|")
		names = vars[:-2:2]
		values = vars[1:-2:2]
		raycasts = list(map(float,vars[-1].split(",")))

		valdict = {"raycasts":raycasts}
		for i in range(len(names)):
			valdict[names[i]] = float(values[i])

		return valdict
	
	def reset(self):
		data = self.conn.recv(1024)
		self.vars = self.parse_vars(data)
		action = {'x':0, 'y':0,'fire':False}

		encoded_action = urllib.parse.urlencode(action)
		response = "HTTP/1.1 " + str(Response(text=encoded_action))
		self.conn.send(response.encode('utf-8'))
		self.fire_count = 0

		return self.get_observation()


	def get_observation(self):
		v = self.vars
		observation = []
		observation += v["raycasts"] # 20
		
		rel_coord_array = [v["w1x"],v["w2x"],v["w1y"],v["w2y"]] #4
		# clamp and normalise coords
		rel_coord_array = list(map(lambda n: ((sorted((-600,n, 600))[1]/600 + 1)/2), rel_coord_array))

		vel_array = [v["vx"],v["vy"],v["w1vx"],v["w2vx"],v["w1vy"],v["w2vy"]] #6
		vel_array = list(map(lambda n: ((sorted((-200,n, 200))[1]/200 + 1)/2), vel_array))

		# 600 is a bit more than the screen height
		y_coord =(sorted((-600,v["y"], 600))[1]/600 + 1)/2  # should be between 0 and 1
		hand = v["hand"]


		observation += vel_array
		observation += rel_coord_array
		observation.append(y_coord)
		observation.append(hand)

		final = np.array(observation)
		return final


	def get_reward(self):
		return self.vars["reward"]


	def get_done(self):
		return self.vars["done"] != 0
