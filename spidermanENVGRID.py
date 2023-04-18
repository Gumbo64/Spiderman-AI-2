from math import cos, pi, sin
import numpy as np
from matplotlib import pyplot as plt
from gym import Env
from gym.spaces import Box

# definitely use these if you want to avoid hassle
import socket
import urllib.parse
from webob import Response
from subprocess import Popen

import platform
from random import random



import os
import time

import csv


class Spiderman_ENV(Env):
	def __init__(self,gameid):
		super().__init__()
		# Setup spaces
		print("ENV",gameid,"made")
		self.gameid = int(gameid)
		self.input_dims = 396
		self.observation_space = Box(low=0, high=1, shape=(self.input_dims,), dtype=np.float64)


		# self.action_space = Box( np.array([-1,-1,-1]), np.array([+1,+1,+1]))
		self.action_space = Box( np.array([-pi,-1]), np.array([+pi,+1]))
			
		self.c = {
			# "N_WINDOWS":10,
			# "WIDTH":500,
			# "HEIGHT":363,
			"WIDTH":800,
			"HEIGHT":800,
			"COOLDOWN":10,
		}
		self.window = None
		self.sock = None
		self.reset()

	def open_windows(self):
		ruffle_launchers = {
			"Linux":"./ruffle",
			"Windows":"./ruffle.exe"
		}

		my_os = platform.system()

		# for i in range(c["N_WINDOWS"]):
		return Popen([ruffle_launchers[my_os], "spidermantrainGRID.swf","--width",str(self.c["WIDTH"]), "--height",str(self.c["HEIGHT"]), "-P","gameid="+str(self.gameid)])


	def step(self, action_array):
		# time.sleep(2)
		# try:
		data = self.conn.recv(2048)
	
		# print(data)
		self.vars = self.parse_vars(data)
		action = {'x': cos(action_array[0]), 'y':sin(action_array[0]),'fire':(action_array[1] > 0)}
		encoded_action = urllib.parse.urlencode(action)
		response = "HTTP/1.1 " + str(Response(text=encoded_action))
		self.conn.send(response.encode('utf-8'))


		# except:
		# 	print("An exception occurred") 
		# 	self.reset()

		observation = self.get_observation()
		done = self.get_done()
		reward = self.get_reward()	
		# print(reward)
		info = {}

		# with open(r'data/data' + str(self.gameid) + '.csv', 'a') as f:
		# 	writer = csv.writer(f)
		# 	writer.writerow(observation)
		
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


		print("-------------------")
		for i in range(16):
			print(   list([ int(i) for i in l] for l in [raycasts[16 * (i-1):16 * i]   ]) )
		
		return valdict
	
	def reset(self):
		if not self.window is None:
			self.sock.close()
			pid = self.window.pid
			os.system("taskkill /f /pid "+str(pid))
			os.system("taskkill /f /pid "+str(pid))
			# os.system("sudo kill -9 "+str(pid))
			# os.system("sudo kill -9 "+str(pid))
		
		self.fire_count=0
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind( ("localhost", 8000 + self.gameid) )

		self.window = self.open_windows()

		# print("listening")
		self.sock.listen()
		# print("listened")
		self.sock.setblocking(False)
		self.sock.settimeout(None)
		self.conn, addr = self.sock.accept()

		# print("stepping")
		self.step([0,0,False])
		# print("stepped")
		
		return self.get_observation()


	def get_observation(self):
		v = self.vars
		observation = []
		observation += v["raycasts"] # 96
		
		rel_coord_array = [v["w1x"],v["w2x"],v["w1y"],v["w2y"]] #4
		# clamp and normalise coords
		rel_coord_array = list(map(lambda n: ((sorted((-600,n, 600))[1]/600 + 1)/2), rel_coord_array))

		vel_array = [v["vx"],v["vy"],v["w1vx"],v["w2vx"],v["w1vy"],v["w2vy"]] #6
		vel_array = list(map(lambda n: ((sorted((-200,n, 200))[1]/200 + 1)/2), vel_array))

		# 600 is a bit more than the screen height
		y_coord =(sorted((-600,v["y"], 600))[1]/600 + 1)/2  # should be between 0 and 1
		linedist = v["linedist"]


		observation += vel_array
		observation += rel_coord_array
		observation.append(y_coord)
		observation.append(linedist)

		final = np.array(observation)
		# print(self.vars)
		# print(final)
		return final


	def get_reward(self):
		return self.vars["reward"]


	def get_done(self):
		return self.vars["done"] != 0

if "__main__" == __name__:
	env = Spiderman_ENV(3)
	env2 = Spiderman_ENV(4)
	while True:
		env.step([1,-1,True])
		env2.step([1,-1,True])
		