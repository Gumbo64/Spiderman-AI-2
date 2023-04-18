import math
def hardAgent(observation):
    theta = 0
    maxt = 0
    shoot = False
    raycasts = observation[:40][::-1]
    for i in range(len(raycasts)):
        if raycasts[i] < 1 and raycasts[i] >= maxt and math.cos(-(i+1) * 9 * math.pi / 180) > -math.cos(math.pi/7) :
            theta = -(i+1) * 9 * math.pi / 180
            maxt = raycasts[i] 
            shoot = True
            break
    return [math.cos(theta),math.sin(theta),shoot]


if __name__ == "__main__":
    from spidermanENV import Spiderman_ENV
    # from hardcodedAGENT import hardAgent
    env = Spiderman_ENV(3)
    observation, reward, done, info = env.step([1,-1,True])
    while True:        
        observation, reward, done, info = env.step(hardAgent(observation))
        if done == True:
            env.reset()


