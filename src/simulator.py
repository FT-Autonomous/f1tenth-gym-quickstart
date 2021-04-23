import time
import yaml
import gym
import numpy as np
from argparse import Namespace
import concurrent.futures

# import your drivers here
from follow_the_gap import GapFollower
from starting_point import SimpleDriver, AnotherDriver

# choose your drivers here (1-4)
drivers = [GapFollower()]

if __name__ == '__main__':
    
    with open('maps/config_example_map.yaml') as file:
        conf_dict = yaml.load(file, Loader=yaml.FullLoader)
    conf = Namespace(**conf_dict)

    env = gym.make('f110_gym:f110-v0', map=conf.map_path,
            map_ext=conf.map_ext, num_agents=len(drivers))# initial reset
    poses = np.array([[-1.25 + (i * 0.75), 0., np.radians(90)] for i in range(len(drivers))]) # specify starting positions of each agent
    obs, step_reward, done, info = env.reset(poses=poses)
    env.render()

    laptime = 0.0
    start = time.time()
    
    while not done:
        actions = []
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, driver in enumerate(drivers):
                futures.append(executor.submit(
                    driver.process_lidar,
                    obs['scans'][i])
                )
        for future in futures:
            speed, steer = future.result()
            actions.append([steer, speed])
        actions = np.array(actions)
        obs, step_reward, done, info = env.step(actions)
        laptime += step_reward
        env.render(mode='human')
    print('Sim elapsed time:', laptime, 'Real elapsed time:', time.time()-start)
