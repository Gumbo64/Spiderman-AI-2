import taichi as ti
import math
import time

ti.init(arch=ti.cuda)


max_steps = 1024

N = 10
segment_length = 0.005
segment_length_idle = 0.001
dt = 1e-5
gravity = 10

x = ti.Vector.field(2, dtype=ti.f32, shape=N)  # particle positions
oldx = ti.Vector.field(2, dtype=ti.f32, shape=N)  
player_field = ti.Vector.field(2,dtype=ti.f32,shape=1)


LMB =  ti.field(dtype=ti.f32, shape=())


player_radius = 0.05

circle_radius = 0.1
circle_radius_squared = circle_radius**2
other_circles = ti.Vector.field(2, dtype=ti.f32, shape=100)
other_circles[0] = [0.75,0.75]

indices = ti.field(dtype=ti.i32,shape=2*N - 1)

def init():
    count = 0
    indices[count]=0
    count+=1
    for i in range(1,N):
        indices[count]=i
        count+=1
        indices[count]=i
        count+=1

    for i in range(0,N):
        a = 0.5
        b = 0.5 + 0.01 * -i
        x[i] = [a,b]
        oldx[i]=[a,b]
    x[N] = [0.5,0.5]




@ti.kernel
def advance():
    
#     put the rest of the advance stuff in the tape too (later on)
    
    if LMB[None] == 1:
        wire_advance(segment_length)
        verlet(N-1)
    else:
        wire_advance(segment_length_idle)
        verlet(N-1)
    
    player_collide(0)    
    
        
        

    
        

@ti.func
def wire_advance(seg_length:ti.f32):
    for i in ti.static(range(0,N-1)):
        r = pull_total(seg_length,i,i+1)
        
        x[i] -= r * 0.5
        x[i+1] += r * 0.5
        verlet(i)
    

@ti.func
def verlet(i: ti.i32):
#         normal verlet integration
    vector = (x[i]-oldx[i]) + dt * ti.Vector([0,-gravity])
    oldx[i] = x[i]
    x[i] += vector
    
    
@ti.func
def pull_total(seg_length:ti.f32,me: ti.i32, them: ti.i32 ):
#         rope constraint (https://youtu.be/FcnvwtyxLds)
        r = (oldx[them]-x[me])
        d = r.norm(1e-6)
        delta_d = seg_length-d
        r *= delta_d/d 
        
        return r

        
    

@ti.func
def player_collide(i: ti.i32):
    diff = (x[i]-other_circles[0])
    distance = diff.norm(1e-6)
    direction =  diff.normalized()
    
    force = max((circle_radius+player_radius)-abs(distance),0)
    
    x[i] += force * direction

def render():
    canvas.set_background_color((0, 0, 0))
    canvas.lines(x, indices=indices, width=0.01,color=(0.2, 0.4, 0.6))
    canvas.circles(x, radius=0.004,color=(1, 1, 1))
    player_field[0] = x[0]
    canvas.circles(player_field, radius=player_radius,color=(1, 0, 0))
    canvas.circles(other_circles, radius=circle_radius,color=(1, 1, 1))
    window.show()



init()
res = (1100, 800)
window = ti.ui.Window("Taichi MLS-MPM-128", res=res, vsync=True)
canvas = window.get_canvas()

mouse_x = 0.5
mouse_y = 0.6


start = time.time()
while window.running:
    
    LMB[None] = 0
    if window.is_pressed(ti.ui.LMB):
        LMB[None]=1
        mouse_x,mouse_y = window.get_cursor_pos()
        x[N-1] = [mouse_x,mouse_y]
        oldx[N-1] = x[N-1]
    advance()

    render()
    time.sleep(0.0166)

