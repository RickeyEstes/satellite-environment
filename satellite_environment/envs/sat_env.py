import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.envs.classic_control import rendering
import numpy as np
from collections import namedtuple
from enum import Enum

_State = namedtuple("_State", "gyros last_angle_reading time_since_reading")

class _Action(Enum):
    CLOCKWISE = 1
    REST = 0
    COUNTER_CLOCKWISE = -1

class _Satellite:
    """
    Object representing the state of a satellite. 
    Assumptions
        - Uses reaction wheels with infinite saturation for attitude adjustment
        - Constant density
        - Motors output constant torque, and the direction of the torque can be changed discontinuously and instantly
    """

    # Mass of the spacecraft in g (arbitrarily chosen)
    MASS = 300.

    # Torque provided by motor controlling reaction wheel (arbitrarily chosen)
    TORQUE = 0.0005 

    # Diameter of spacecraft in cm
    LENGTH = 5.

    # Height of spacecraft in mm
    HEIGHT = 2

    # When angular velocity is low enough, a real satellite could use camera data and sun sensors to get the
    # absolute attitude. This variable holds the maximum such velocity before the cameras would be useless
    MAX_V_FOR_READING = 0.001

    def __init__(self):
        # Initialize angular velocity (arbitrarily chosen)
        self.angular_velocity = 0.3

        # Initialize orientation of satellite in radians to a horizontal position
        self.angle = 0.3

        # Renders the satellite
        self.viewer = None

        # Last 5 readings of the angle of the satellite from the horizontal, with a small amount of noise; gets
        # initialized to some garbage value. Most recent is first. 
        self.gyro_readings = (0, 0, 0, 0, 0)

        self.last_angle_reading = 0

        # The time elapsed since the satellite was stable enough for a reliable angle reading
        self.time_since_last_reading = 0

    def getstate(self):
        return _State(self.gyro_readings, self.last_angle_reading, self.time_since_last_reading)

    def step(self, a):
        """
        Updates the satellite from action a
        """
        
        # Calculates torque based on action
        torque = 0
        if(a == _Action.CLOCKWISE):
            torque = self.TORQUE
        elif(a == _Action.COUNTER_CLOCKWISE):
            torque = -self.TORQUE
        elif(a == _Action.REST):
            torque = 0

        # Calculates angular acceleration
        angular_acceleration = torque / self.MASS * 1000
        self.angular_velocity += angular_acceleration

        # Increments angle
        self.angle += self.angular_velocity

        # Injects a small amount of noise to gyro readings using a normal distribution
        curr_reading = self.angular_velocity + np.random.normal(scale = 0.00001)

        # Updates gyro readings
        self.gyro_readings = (curr_reading,) + self.gyro_readings[0:4]

        # Updates absolute attitude determination if angular velocity is low enough
        if(abs(self.angular_velocity) < self.MAX_V_FOR_READING):
            # Adds noise to reading
            self.last_angle_reading = (self.angle + np.random.normal(scale = 0.0001)) % (2 * np.pi)

            # Reset counter storing time between readings
            self.time_since_last_reading = 0
        
        else:
            self.time_since_last_reading += 1


    def render(self, mode='human'):
        # Initializes and configures renderer
        if self.viewer is None:
            self.viewer = rendering.Viewer(600,600)
            bound = self.LENGTH / 100 + 0.002
            self.viewer.set_bounds(-bound, bound, -bound, bound)

        # Draws satellite body on coordinate plane 
        left = -self.LENGTH / 200.
        right = self.LENGTH / 200. 
        top = self.HEIGHT / 2000.
        bottom = -self.HEIGHT / 2000. 
        sat = self.viewer.draw_polygon([(left, bottom), (left, top), (right, top), (right, bottom)])
        sat.set_color(0, 0, 0)
        transform = rendering.Transform(rotation=self.angle)
        sat.add_attr(transform)

        self.viewer.render()

s = _Satellite()
while True:
    a = 0
    if s.getstate()[0][0] < 0:
        a = _Action.CLOCKWISE
    else:
        a = _Action.COUNTER_CLOCKWISE
    s.step(a)
    s.render()

class SatEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # TODO Implement
        pass

    # TODO Implement
    def step(self, action):
        """
        Returns:
            A 4 element list:
                - Next state
                - Reward
                - Boolean stating if model is done
                - Other data
        """
        pass
        
    def reset(self):
        # TODO Implement
        pass
        
    def render(self, mode='human', close=False):
        # TODO Implement
        pass
