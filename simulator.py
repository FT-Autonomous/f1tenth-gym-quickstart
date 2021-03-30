from follow_the_gap import GapFollower
import time
import yaml
import gym
import numpy as np
from argparse import Namespace

if __name__ == '__main__':

    work = {'mass': 3.463388126201571, 'lf': 0.15597534362552312,
            'tlad': 0.82461887897713965, 'vgain': 0.90338203837889}
    with open('config_example_map.yaml') as file:
        conf_dict = yaml.load(file, Loader=yaml.FullLoader)
    conf = Namespace(**conf_dict)

    env = gym.make('f110_gym:f110-v0', map=conf.map_path,
            map_ext=conf.map_ext, num_agents=1)# s_min=-np.pi, s_max=np.pi)
    obs, step_reward, done, info = env.reset(np.array([[conf.sx, conf.sy,
        conf.stheta]]))
    env.render()
    planner = GapFollower()

    laptime = 0.0
    start = time.time()
    
    while not done:
        speed, steer = planner.lidar_callback(obs['scans'][0])
        obs, step_reward, done, info = env.step(np.array([[steer/2, speed]]))
        laptime += step_reward
        env.render(mode='human')
    print('Sim elapsed time:', laptime, 'Real elapsed time:', time.time()-start)
