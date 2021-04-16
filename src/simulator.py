import time
import yaml
import gym
import numpy as np
from argparse import Namespace

# import your drivers here
from follow_the_gap import GapFollower
from starting_point import SimpleDriver, AnotherDriver

# choose your driver here
driver = GapFollower()

if __name__ == '__main__':
    
    with open('maps/config_example_map.yaml') as file:
        conf_dict = yaml.load(file, Loader=yaml.FullLoader)
    conf = Namespace(**conf_dict)

    env = gym.make('f110_gym:f110-v0', map=conf.map_path,
            map_ext=conf.map_ext, num_agents=1)
    obs, step_reward, done, info = env.reset(np.array([[conf.sx, conf.sy,
        conf.stheta]]))
    env.render()

    laptime = 0.0
    start = time.time()
    
    while not done:
        speed, steer = driver.process_lidar(obs['scans'][0])
        obs, step_reward, done, info = env.step(np.array([[steer, speed]]))
        laptime += step_reward
        env.render(mode='human')
    print('Sim elapsed time:', laptime, 'Real elapsed time:', time.time()-start)
