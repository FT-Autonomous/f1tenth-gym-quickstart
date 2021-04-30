import numpy as np


# drives straight ahead at a speed of 5
class SimpleDriver:    

    def process_lidar(self, ranges):
        speed = 5.0
        steering_angle = 0.0
        return speed, steering_angle


# drives toward the furthest point it sees
class AnotherDriver:

    def process_lidar(self, ranges):
        # the number of LiDAR points
        NUM_RANGES = len(ranges)
        # angle between each LiDAR point
        ANGLE_BETWEEN = 2*np.pi / NUM_RANGES
        # number of points in each quadrant
        NUM_PER_QUADRANT = NUM_RANGES // 4

        # the index of the furthest LiDAR point (ignoring the points behind the car)
        max_idx = np.argmax(ranges[NUM_PER_QUADRANT:-NUM_PER_QUADRANT]) + NUM_PER_QUADRANT
        # some math to get the steering angle to correspond to the chosen LiDAR point
        steering_angle = max_idx*ANGLE_BETWEEN - (NUM_RANGES//2)*ANGLE_BETWEEN
        speed = 5.0
        
        return speed, steering_angle
