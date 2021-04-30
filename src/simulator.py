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

# choose your racetrack here (TRACK_1, TRACK_2, TRACK_3, OBSTACLES)
RACETRACK = 'TRACK_1'

if __name__ == '__main__':
    with open('maps/{}.yaml'.format(RACETRACK)) as map_conf_file:
        map_conf = yaml.load(map_conf_file, Loader=yaml.FullLoader)
    origin = map_conf['origin']
    env = gym.make('f110_gym:f110-v0', map="maps/{}".format(RACETRACK),
            map_ext=".png", num_agents=len(drivers))
    # specify starting positions of each agent
    poses = np.array([[-1.25 + (i * 0.75), 0., np.radians(90)] for i in range(len(drivers))])
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
