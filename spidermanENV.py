
# environment
from click import option
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from gym import Env
from gym.spaces import Box, Discrete

import socket
import time
import urllib.parse
from random import random
from subprocess import Popen
import platform
from collections import defaultdict
from webob import Response
import selectors


import os 




class Spiderman_ENV(Env):
	def __init__(self):
		super().__init__()
		# Setup spaces
		
		self.input_dims = 32
		self.observation_space = Box(low=0, high=1, shape=self.input_dims, dtype=np.float32)

		# 20 grid positions + none
		self.action_space = Box( np.array([0,0]), np.array([+1,+1]))

		self.last_score=295
			
		self.c = {
			# "N_WINDOWS":10,
			# "WIDTH":500,
			# "HEIGHT":363,
			"WIDTH":300,
			"HEIGHT":300,
		}


		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(("localhost", 8000))

		self.open_windows()

		sock.listen()
		sock.setblocking(False)
		sock.settimeout(None)
		self.conn, addr = sock.accept()



	def step(self, action):
		data = self.conn.recv(1024)
		self.vars = self.parse_vars(data)
		
		done = self.vars["done"]


		
		
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
		return self.get_observation()



	def get_observation(self):
		# get an updated image of the game
		
		return np.resize(blackAndWhiteImage, self.input_dims)


	def get_reward(self):
		

		reward = score - self.last_score
		self.last_score=score
		# print(reward)
		return reward
	# def get_score(self):
	# 	return self.lastscore

	def get_done(self,observation):
		# print(np.sum(observation)/255)
		if np.sum(observation)/255 > 6000:
			return True
		return False
