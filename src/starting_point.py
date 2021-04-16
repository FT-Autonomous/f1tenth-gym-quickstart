import numpy as np

class SimpleDriver:    

    def process_lidar(self, ranges):
        speed = 5.0
        steering_angle = 0.0
        return speed, steering_angle

class AnotherDriver:

    def process_lidar(self, ranges):
        NUM_RANGES = len(ranges)
        ANGLE_BETWEEN = 2*np.pi / NUM_RANGES
        NUM_PER_QUADRANT = NUM_RANGES // 4

        max_idx = np.argmax(ranges[NUM_PER_QUADRANT:-NUM_PER_QUADRANT]) + NUM_PER_QUADRANT
        steering_angle = max_idx*ANGLE_BETWEEN - (NUM_RANGES//2)*ANGLE_BETWEEN
        speed = 5.0
        
        return speed, steering_angle
