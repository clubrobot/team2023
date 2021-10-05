#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event

from listeners.position_listener import *
from listeners.sensor_listener import *
from common.roadmap import intersect
from logs.log_manager import *
import math
import time


class AviodanceBehaviour(Thread):

    # Avoiding behaviour
    BEHAVIOUR_STOPPING = 0
    BEHAVIOUR_AVOID = 1
    # TODO : Add new behaviour here

    # Avoiding detection style
    BEHAVIOUR_DETECT_NEAR_TO_ME = 0
    BEHAVIOUR_DETECT_ON_MY_PATH = 1

    # Direction
    FORWARD = 1
    BACKWARD = -1

    # State
    INIT = 0
    RUN = 1

    def __init__(self, wheeledbase, roadmap, beacon_client, sensors, behaviour=BEHAVIOUR_STOPPING, timestep=0.1, exec_param=Logger.SHOW, log_level=INFO):
        """
            Init all internals components
        """
        Thread.__init__(self)
        self.daemon = True

        # Init Logger
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        # Create path
        self.path = None

        # Internal state
        self.state = self.INIT

        # Default direction
        self.direction = self.FORWARD

        # Init internal events
        self.on_brother_moving_event = Event()
        self.on_opponentA_moving_event = Event()
        self.on_opponentB_moving_event = Event()

        self.on_left_event = Event()
        self.on_mid_left_event = Event()
        self.on_mid_right_event = Event()
        self.on_right_event = Event()

        self.abort = Event()

        # Stopping event
        self.stop = Event()

        # Clear all internal events
        self.on_brother_moving_event.clear()
        self.on_opponentA_moving_event.clear()
        self.on_opponentB_moving_event.clear()

        self.on_left_event.clear()
        self.on_mid_left_event.clear()
        self.on_mid_right_event.clear()
        self.on_right_event.clear()

        # Bind behaviour wheeledbase and beacon client
        self.wheeledbase = wheeledbase
        self.roadmap = roadmap
        self.beacon_client = beacon_client
        self.sensors = sensors
        self.behaviour = behaviour
        self.timestep = timestep  # Seconds

        # subscribe to the sensors topic
        # try:
        #     ret = self.sensors.subscribeSensors()
        #     self.logger(INFO, 'Subscribe to the sensors topics', status=ret)
        # except:
        #     self.logger(
        #         CRITICAL, 'Cannot subsribe to the topic handler, no opponent detection')

        # Instanciate position listener
        self.position_listener = PositionListener(
            self.beacon_client.get_brother_pos, self.beacon_client.get_opponents_pos)

        # Instanciate Sensors listener
        self.sensor_listener = SensorListener(
            self._left_sensor_wrapper, self._mid_left_sensor_wrapper, self._mid_right_sensor_wrapper, self._right_sensor_wrapper, threshold=300)

        # Bind internal event generator
        self.position_listener.bind(
            PositionListener.BROTHER, self._on_brother_moving)
        self.position_listener.bind(
            PositionListener.OPPONENTA, self._on_opponentA_moving)
        self.position_listener.bind(
            PositionListener.OPPONENTB, self._on_opponentB_moving)

        self.sensor_listener.bind(
            SensorListener.LEFT, self._on_left_obstacle)
        self.sensor_listener.bind(
            SensorListener.MID_LEFT, self._on_mid_left_obstacle)
        self.sensor_listener.bind(
            SensorListener.MID_RIGHT, self._on_mid_right_obstacle)
        self.sensor_listener.bind(
            SensorListener.RIGHT, self._on_right_obstacle)

        # Instanciate obstacles
        self.friend_obstacle = self.roadmap.create_obstacle(
            ((-200, -200), (200, -200), (200, 200), (-200, 200)))
        self.opp_A_obstacle = self.roadmap.create_obstacle(
            ((-200, -200), (200, -200), (200, 200), (-200, 200)))
        self.opp_B_obstacle = self.roadmap.create_obstacle(
            ((-200, -200), (200, -200), (200, 200), (-200, 200)))
        # Sensor obstacle is bigger because we can't exactly know its center position
        self.sensor_obstacle = self.roadmap.create_obstacle(
            ((-400, -400), (400, -400), (400, 400), (-400, 400)))

        self.friend_obstacle.set_position(-1000, -1000)
        self.opp_A_obstacle.set_position(-1000, -1000)
        self.opp_B_obstacle.set_position(-1000, -1000)
        self.sensor_obstacle.set_position(-1000, -1000)

        self.start()

    def _left_sensor_wrapper(self):
        """
            Always return left sensor value depending to the robot direction
        """
        if self.direction == self.FORWARD:
            return self.sensors.get_range_left_front()
        else:
            return self.sensors.get_range_left_back()

    def _mid_left_sensor_wrapper(self):
        """
            Always return mid left sensor value depending to the robot direction
        """
        if self.direction == self.FORWARD:
            return self.sensors.get_sensor3_range()
        else:
            return self.sensors.get_sensor1_range()

    def _mid_right_sensor_wrapper(self):
        """
            Always return mid right sensor value depending to the robot direction
        """
        if self.direction == self.FORWARD:
            return self.sensors.get_sensor4_range()
        else:
            return self.sensors.get_sensor2_range()

    def _right_sensor_wrapper(self):
        """
            Always return right sensor value depending to the robot direction
        """
        if self.direction == self.FORWARD:
            return self.sensors.get_range_right_front()
        else:
            return self.sensors.get_range_right_back()

    def _on_brother_moving(self):
        """
            Generate Event when Brother moving
        """
        self.on_brother_moving_event.set()

    def _on_opponentA_moving(self):
        """
            Generate Event when opponentA moving
        """
        self.on_opponentA_moving_event.set()

    def _on_opponentB_moving(self):
        """
            Generate Event when opponentA moving
        """
        self.on_opponentB_moving_event.set()

    def _on_left_obstacle(self):
        """
            Generate Event on left obstacle
        """
        self.on_left_event.set()

    def _on_mid_left_obstacle(self):
        """
            Generate Event on mid left obstacle
        """
        self.on_mid_left_event.set()

    def _on_mid_right_obstacle(self):
        """
            Generate Event on mid right obstacle
        """
        self.on_mid_right_event.set()

    def _on_right_obstacle(self):
        """
            Generate Event on right obstacle
        """
        self.on_right_event.set()

    def _is_on_my_path(self, obstacle):
        """
        Check if the obstacle intersect the current path
        """
        if self.path is not None:
            shape = obstacle.get_shape()
            for i in range(len(self.path) - 1):
                edge = self.path[i], self.path[i+1]
                for i in range(len(shape)):
                    cutline = (shape[i], shape[(i + 1) % len(shape)])
                    if intersect(cutline, edge):
                        self.logger(WARNING, 'obstacle is on the path')
                        return True
                    else:
                        self.logger(INFO, 'cutline is not on the path')

            self.logger(INFO, 'obstacle is not on the path')
            return False
        else:
            return False

    def run(self):
        while not self.stop.is_set():
            # Check opponents only on running state
            if self.state == self.RUN:
                # when the beahaviour is stopping, only stop the robot and wait
                if self.behaviour == self.BEHAVIOUR_STOPPING:
                    while self.on_left_event.is_set() or self.on_mid_left_event.is_set() or self.on_mid_right_event.is_set() or self.on_right_event.is_set():
                        self.logger(WARNING, "Obstacle on my path !")
                        self.abort.set()
                        self.on_left_event.clear()
                        self.on_mid_left_event.clear()
                        self.on_mid_right_event.clear()
                        self.on_right_event.clear()
                        sleep(self.timestep)

                    if self.abort.is_set():
                        self.abort.clear()
                        self.logger(INFO, "No Obstacle !",)

                else:
                    # NOT CURRENTLY TESTED ON REAL ROBOT, use BEHAVIOUR_STOPPING instead
                    if self.on_brother_moving_event.is_set():
                        self.logger(INFO, "Brother is moving ...", pos=self.position_listener.get_position(
                            PositionListener.BROTHER))

                        self.friend_obstacle.set_position(
                            *self.position_listener.get_position(PositionListener.BROTHER))
                        if(self._is_on_my_path(self.friend_obstacle)):
                            self.abort.set()

                        self.on_brother_moving_event.clear()

                    if self.on_opponentA_moving_event.is_set():
                        self.logger(INFO, "OpponentA is moving ...", pos=self.position_listener.get_position(
                            PositionListener.OPPONENTA))

                        self.opp_A_obstacle.set_position(
                            *self.position_listener.get_position(PositionListener.OPPONENTA))
                        if(self._is_on_my_path(self.opp_A_obstacle)):
                            self.abort.set()

                        self.on_opponentA_moving_event.clear()

                    if self.on_opponentB_moving_event.is_set():
                        self.logger(INFO, "OpponentB is moving ...", pos=self.position_listener.get_position(
                            PositionListener.OPPONENTB))

                        self.opp_B_obstacle.set_position(
                            *self.position_listener.get_position(PositionListener.OPPONENTB))
                        if(self._is_on_my_path(self.opp_B_obstacle)):
                            self.abort.set()

                        self.on_opponentB_moving_event.clear()

                    if self.on_left_event.is_set():
                        # Compute the obstacle position

                        # Get the sensor pos with the wrapper : self._left_sensor_wrapper()
                        # This function return the projected point relative to the center of the robot
                        # Get the wheeledbase position and project point on real map
                        self.logger(WARNING, "Obstacle on my left ...",
                                    dist=self._left_sensor_wrapper())
                        # self.sensor_obstacle.set_position(871, 1919)
                        if(self._is_on_my_path(self.sensor_obstacle)):
                            self.abort.set()
                        self.on_left_event.clear()

                    if self.on_mid_left_event.is_set():
                        # Compute the obstacle position
                        self.logger(WARNING, "Obstacle on my mid left ...",
                                    dist=self._mid_left_sensor_wrapper())
                        if(self._is_on_my_path(self.sensor_obstacle)):
                            self.abort.set()
                        self.on_mid_left_event.clear()

                    if self.on_mid_right_event.is_set():
                        # Compute the obstacle position
                        self.logger(WARNING, "Obstacle on my mid right ...",
                                    dist=self._mid_right_sensor_wrapper())
                        if(self._is_on_my_path(self.sensor_obstacle)):
                            self.abort.set()
                        self.on_mid_right_event.clear()

                    if self.on_right_event.is_set():
                        # Compute the obstacle position
                        self.logger(WARNING, "Obstacle on my right ...",
                                    dist=self._right_sensor_wrapper())
                        if(self._is_on_my_path(self.sensor_obstacle)):
                            self.abort.set()
                        self.on_right_event.clear()

                sleep(self.timestep)

    def move(self, destination, thresholds=(None, None)):
        linpos_threshold, angpos_threshold = thresholds
        default_linpos_threshold = 3
        default_angpos_threshold = 0.1

        # Set state to run
        self.state = self.RUN

        # Pathfinding
        path_not_found = False
        x_in, y_in, theta_in = self.wheeledbase.get_position()
        x_sp, y_sp, theta_sp = destination

        try:
            self.path = self.roadmap.get_shortest_path(
                (x_in, y_in), (x_sp, y_sp))
            self.logger(INFO, 'follow path: [{}]'.format(', '.join(
                '({0[0]:.0f}, {0[1]:.0f})'.format(waypoint) for waypoint in self.path)))
        except RuntimeError:
            path_not_found = True

        # Return there is no path available
        if path_not_found:
            self.logger(ERROR, 'No path found !')
            sleep(1)
            return False

        # Pure Pursuit configuration
        if math.cos(math.atan2(self.path[1][1] - self.path[0][1], self.path[1][0] - self.path[0][0]) - theta_in) >= 0:
            self.logger(INFO, 'Moving forward !')
            self.direction = self.FORWARD
        else:
            self.logger(INFO, 'Moving backward !')
            self.direction = self.BACKWARD

        if math.hypot(self.path[1][0] - self.path[0][0], self.path[1][1] - self.path[0][1]) < 5 and theta_sp is not None:
            finalangle = theta_sp - (self.direction - 1) * math.pi
        else:
            finalangle = None

        self.wheeledbase.lookahead.set(150)
        self.wheeledbase.lookaheadbis.set(150)
        self.wheeledbase.max_linvel.set(300)
        self.wheeledbase.max_angvel.set(6.0)
        self.wheeledbase.linpos_threshold.set(
            linpos_threshold or default_linpos_threshold)
        self.wheeledbase.angpos_threshold.set(
            angpos_threshold or default_angpos_threshold)

        # Trajectory
        self.wheeledbase.purepursuit(self.path, direction={
                                     self.FORWARD: 'forward', self.BACKWARD: 'backward'}[self.direction], finalangle=finalangle)

        # Wait until destination is reached
        isarrived = False
        blocked = False
        while not isarrived:

            try:
                isarrived = self.wheeledbase.isarrived()
            except RuntimeError:
                self.logger(WARNING, 'Blocked while following path')
                blocked = True

            # If obstacle is on my path abort
            if self.behaviour == self.BEHAVIOUR_STOPPING:
                if self.abort.is_set():
                    timeout = time.time() + 5   # 5 seconds timemout
                    self.wheeledbase.stop()
                    while self.abort.is_set():
                        self.logger(INFO, 'Wait ...')
                        if time.time() > timeout:
                            self.logger(INFO, 'Timeout ! Retry to move')
                            return False
                        sleep(1)
                    self.logger(INFO, 'Continue ...')
                    return False
            else:
                if self.abort.is_set():
                    self.wheeledbase.stop()
                    self.abort.clear()
                    return False

            if blocked:
                self.logger(INFO, 'Go backward a little')
                self.wheeledbase.set_velocities(-self.direction * 100, 0)
                sleep(1)
                self.logger(INFO, 'Resume path')
                self.wheeledbase.purepursuit(
                    self.path, direction={self.FORWARD: 'forward', self.BACKWARD: 'backward'}[self.direction])
                blocked = False

        # Everything is fine
        self.wheeledbase.linpos_threshold.set(default_linpos_threshold)
        self.wheeledbase.angpos_threshold.set(default_angpos_threshold)

        return True
