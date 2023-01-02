# Main resources
# https://github.com/taichi-dev/taichi/blob/master/python/taichi/examples/autodiff/minimization.py

from datetime import datetime 

start_time = datetime.now() 
import sys
# sys.tracebacklimit=0


import random

import taichi as ti
import time 

ti.init(arch=ti.gpu)
# ti.init(arch=ti.cpu,cpu_max_num_threads=1,debug=True)


N = 4
T = 10

u = ti.Vector.field(n=2,dtype=ti.f32, shape=(), needs_grad=True)
pos = ti.Vector.field(n=2,dtype=ti.f32, shape=(T,N),needs_grad=True)
d_pos = ti.Vector.field(n=2,dtype=ti.f32, shape=(T,N),needs_grad=True)

L = ti.field(dtype=ti.f32, shape=(), needs_grad=True)

# u = ti.Vector.field(n=2,dtype=ti.f32, shape=())
# pos = ti.Vector.field(n=2,dtype=ti.f32, shape=(T,N))
# d_pos = ti.Vector.field(n=2,dtype=ti.f32, shape=(T,N))

# L = ti.field(dtype=ti.f32, shape=())

@ti.func
def F_spring(vec):  # Force of spring, see https://youtu.be/FcnvwtyxLds?t=612
    spring_k=1
    l=10
    return spring_k*( vec.norm(1e-6) - l) * vec.normalized(1e-6) 

@ti.kernel
def simulate():
#   pos[0] (initial conditions) is already done
    for t in ti.static(range(1,T)):
        for i in ti.static(range(1,N)):
#         verlet integration on all rope segments
#                 d_pos[t,i] += pos[t-1,i]-pos[t-2,i] + ti.Vector([0,10])
            d_pos[t,i] += d_pos[t-1,i] + ti.Vector([0,10])

        ######     Constraints

        
        d_pos[t,0] += (u[None] - pos[t-1,0]) * 0.25
        
        for i in ti.static(range(1,N-1)):
            v1 = F_spring(pos[t-1,i-1] - pos[t-1,i]) * 0.5
            v2 = F_spring(pos[t-1,i+1] - pos[t-1,i]) * 0.5
            d_pos[t,i] += (v1 + v2)
#             print('i =', i)
        
#         REMEMBER THE LARGER ONE (N-1) IS ON THE RIGHT
        v1 = F_spring(pos[t-1,(N-1)-1] - pos[t-1,N-1]) * 0.5
        d_pos[t,N-1] += v1
        
        for i in ti.static(range(N)):
            pos[t,i] += d_pos[t,i]

        
@ti.kernel
def compute_loss():
    for t in ti.static(range(T)):
        L[None] += t * (pos[t,N-1] - ti.Vector([120.0,60.0])).norm(1e-6)
#     L[None] += (pos[T-1,N-1] - ti.Vector([120.0,60.0])).norm(1e-6)
        

@ti.kernel
def gradient_descent():
    for d in ti.static(range(2)):
        u[None][d] -= 0.1 * u.grad[None][d]
#         print(u.grad[None][d])


def main():
    # Initialize positions of rope segments
    for i in range(N):
        pos[0,i] = [i * random.random() * 100,i * random.random() * 100]
        d_pos[0,i] = [0,0]
    u[None] = [50,50]
    
    # Optimize with m gradient descent iterations
    for k in range(1):
        with ti.ad.Tape(loss=L):
            simulate()
            compute_loss()
            
            gradient_descent()

            print("-----u------")
            print('Loss =', L[None]," ",k)
            print(u)
            print(u.grad[None])

            time_elapsed = datetime.now() - start_time 
            print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))



main()
    

# import pygame
# import time
# import math


# magnification = 1

# def render(t):
    
#     list_pos = [ [pos[t,i].x/magnification + 500,pos[t,i].y/magnification + 500] for i in range(N) ]
# #     print(list_pos)
    
#     window.fill((255, 255, 255))
    
    
#     for pair in list(zip(list_pos, list_pos[1:])):
#         pygame.draw.line(window, (0,0,0), pair[0], pair[1],width=5)
#     for p in list_pos[:-1]:
#         pygame.draw.circle(window, (0, 255, 0),list(p), 10, 0)
#     pygame.draw.circle(window, (255, 0, 0),list(list_pos[N-1]), 10, 0)
    
# #     pygame.draw.circle(window, (255, 0, 0),list(anchor), 5, 0)
#     # Draws the surface object to the screen.
#     img = font.render(str(t), True,(0, 0, 0))
#     window.blit(img, (20, 20))
    
#     pygame.display.update()

# pygame.init()
# font = pygame.font.SysFont(None, 40)
# window = pygame.display.set_mode((1000, 1000))
# run = True
# while run:
#     for t in range(T):
# #         print(t)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#         render(t)
#         time.sleep(0.0167 * 5)
