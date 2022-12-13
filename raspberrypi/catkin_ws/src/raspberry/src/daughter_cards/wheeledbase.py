#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from ctypes.wintypes import BOOL
import time
import math

import rospy
from common.serialutils import Deserializer
from common.serialtalks import BYTE, LONG, FLOAT
from daughter_cards.arduino import SecureArduino
from std_msgs.msg import String
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from std_msg.msg import tos_data

# Instructions
SET_VELOCITIES_OPCODE           = "wheelbase/SET_VELOCITIES"

START_PUREPURSUIT_OPCODE        = "wheelbase/START_PUREPURSUIT"
START_TURNONTHESPOT_OPCODE      = "wheelbase/START_TURNONTHESPOT"

SET_OPENLOOP_VELOCITIES_OPCODE  = "wheelbase/SET_OPENLOOP_VELOCITIES"

POSITION_REACHED_OPCODE         = "wheelbase/POSITION_REACHED"

SET_POSITION_OPCODE	            = "wheelbase/SET_POSITION"


SET_PARAMETER_VALUE_OPCODE      = "wheelbase/SET_PARAMETER_VALUE"
GET_PARAMETER_VALUE_OPCODE      = "wheelbase/GET_PARAMETER_VALUE"

GET_POSITION_OPCODE	            = "wheelbase/GET_POSITION"
GET_VELOCITIES_OPCODE           = "wheelbase/GET_VELOCITIES"

GET_CODEWHEELS_COUNTERS_OPCODE  = "wheelbase/GET_CODEWHEELS_COUNTERS"
GET_VELOCITIES_WANTED_OPCODE    = "wheelbase/GET_VELOCITIES_WANTED"

RESET_PUREPURSUIT_OPCODE        = "wheelbase/RESET_PUREPURSUIT"
ADD_PUREPURSUIT_WAYPOINT_OPCODE = "wheelbase/ADD_PUREPURSUIT_WAYPOINT"

GOTO_DELTA_OPCODE               = "wheelbase/GOTO_DELTA"
RESET_PARAMETERS_OPCODE         = "wheelbase/RESET_PARAMETERS"
SAVE_PARAMETERS_OPCODE          = "wheelbase/SAVE_PARAMETERS"

START_TURNONTHESPOT_DIR_OPCODE = "wheelbase/START_TURNONTHESPOT_DIR"

LEFTWHEEL_RADIUS_ID	            = 0x10
LEFTWHEEL_CONSTANT_ID           = 0x11
LEFTWHEEL_MAXPWM_ID             = 0x12
RIGHTWHEEL_RADIUS_ID            = 0x20
RIGHTWHEEL_CONSTANT_ID          = 0x21
RIGHTWHEEL_MAXPWM_ID            = 0x22
LEFTCODEWHEEL_RADIUS_ID	        = 0x40
LEFTCODEWHEEL_COUNTSPERREV_ID   = 0x41
RIGHTCODEWHEEL_RADIUS_ID        = 0x50
RIGHTCODEWHEEL_COUNTSPERREV_ID  = 0x51
ODOMETRY_AXLETRACK_ID           = 0x60
ODOMETRY_SLIPPAGE_ID            = 0x61
VELOCITYCONTROL_AXLETRACK_ID    = 0x80
VELOCITYCONTROL_MAXLINACC_ID    = 0x81
VELOCITYCONTROL_MAXLINDEC_ID    = 0x82
VELOCITYCONTROL_MAXANGACC_ID    = 0x83
VELOCITYCONTROL_MAXANGDEC_ID    = 0x84
VELOCITYCONTROL_SPINSHUTDOWN_ID = 0x85
LINVELPID_KP_ID                 = 0xA0
LINVELPID_KI_ID                 = 0xA1
LINVELPID_KD_ID                 = 0xA2
LINVELPID_MINOUTPUT_ID          = 0xA3
LINVELPID_MAXOUTPUT_ID          = 0xA4
ANGVELPID_KP_ID                 = 0xB0
ANGVELPID_KI_ID                 = 0xB1
ANGVELPID_KD_ID                 = 0xB2
ANGVELPID_MINOUTPUT_ID	        = 0xB3
ANGVELPID_MAXOUTPUT_ID	        = 0xB4
POSITIONCONTROL_LINVELKP_ID     = 0xD0
POSITIONCONTROL_ANGVELKP_ID     = 0xD1
POSITIONCONTROL_LINVELMAX_ID    = 0xD2
POSITIONCONTROL_ANGVELMAX_ID    = 0xD3
POSITIONCONTROL_LINPOSTHRESHOLD_ID  = 0xD4
POSITIONCONTROL_ANGPOSTHRESHOLD_ID  = 0xD5
PUREPURSUIT_LOOKAHEAD_ID        = 0xE0
PUREPURSUIT_LOOKAHEADBIS_ID     = 0xE2


"""
This class acts as an interface between the raspeberry pi and the arduino.
It contains methods for each action of the wheeled base. 
It allows the raspeberry pi to ask the arduino to perform an action via a specific OPCODE.
"""
class WheeledBase(SecureArduino):

    _DEFAULT = {
        GET_CODEWHEELS_COUNTERS_OPCODE : Deserializer(LONG(0) + LONG(0)),
        POSITION_REACHED_OPCODE : Deserializer(BYTE(0) + BYTE(0)),
        GET_VELOCITIES_WANTED_OPCODE : Deserializer(FLOAT(0) + FLOAT(0)),
        GET_POSITION_OPCODE : Deserializer(FLOAT(0) + FLOAT(0)+ FLOAT(0)),
        GET_VELOCITIES_OPCODE :  Deserializer(FLOAT(0) + FLOAT(0)),
        GET_PARAMETER_VALUE_OPCODE : Deserializer(LONG(0) + LONG(0))

    }

    FORWARD = 1
    BACKWARD = 2
    NO_DIR = 0

    LATCH_TIMESTEP = 0.2

    class Parameter():
        def __init__(self, parent, id, type):
            self.parent = parent
            self.id   = id
            self.type = type
        def get(self): return self.parent.get_parameter_value(self.id, self.type)
        def set(self, value): self.parent.set_parameter_value(self.id, value, self.type)

    def __init__(self, parent, uuid='wheeledbase'):
        SecureArduino.__init__(self, parent, uuid, WheeledBase._DEFAULT)

        self.left_wheel_radius              = WheeledBase.Parameter(self, LEFTWHEEL_RADIUS_ID, FLOAT)
        self.left_wheel_constant            = WheeledBase.Parameter(self, LEFTWHEEL_CONSTANT_ID, FLOAT)
        self.left_wheel_maxPWM              = WheeledBase.Parameter(self, LEFTWHEEL_MAXPWM_ID, FLOAT)

        self.right_wheel_radius             = WheeledBase.Parameter(self, RIGHTWHEEL_RADIUS_ID, FLOAT)
        self.right_wheel_constant           = WheeledBase.Parameter(self, RIGHTWHEEL_CONSTANT_ID, FLOAT)
        self.right_wheel_maxPWM             = WheeledBase.Parameter(self, RIGHTWHEEL_MAXPWM_ID, FLOAT)

        self.left_codewheel_radius          = WheeledBase.Parameter(self, LEFTCODEWHEEL_RADIUS_ID, FLOAT)
        self.left_codewheel_counts_per_rev  = WheeledBase.Parameter(self, LEFTCODEWHEEL_COUNTSPERREV_ID, LONG)

        self.right_codewheel_radius         = WheeledBase.Parameter(self, RIGHTCODEWHEEL_RADIUS_ID, FLOAT)
        self.right_codewheel_counts_per_rev = WheeledBase.Parameter(self, RIGHTCODEWHEEL_COUNTSPERREV_ID, LONG)

        self.codewheels_axletrack           = WheeledBase.Parameter(self, ODOMETRY_AXLETRACK_ID, FLOAT)
        self.odometry_slippage              = WheeledBase.Parameter(self, ODOMETRY_SLIPPAGE_ID, FLOAT)

        self.wheels_axletrack               = WheeledBase.Parameter(self, VELOCITYCONTROL_AXLETRACK_ID, FLOAT)
        self.max_linacc                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXLINACC_ID, FLOAT)
        self.max_lindec                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXLINDEC_ID, FLOAT)
        self.max_angacc                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXANGACC_ID, FLOAT)
        self.max_angdec                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXANGDEC_ID, FLOAT)
        self.spin_shutdown                  = WheeledBase.Parameter(self, VELOCITYCONTROL_SPINSHUTDOWN_ID, BYTE)

        self.linvel_KP                      = WheeledBase.Parameter(self, LINVELPID_KP_ID, FLOAT)
        self.linvel_KI                      = WheeledBase.Parameter(self, LINVELPID_KI_ID, FLOAT)
        self.linvel_KD                      = WheeledBase.Parameter(self, LINVELPID_KD_ID, FLOAT)

        self.angvel_KP                      = WheeledBase.Parameter(self, ANGVELPID_KP_ID, FLOAT)
        self.angvel_KI                      = WheeledBase.Parameter(self, ANGVELPID_KI_ID, FLOAT)
        self.angvel_KD                      = WheeledBase.Parameter(self, ANGVELPID_KD_ID, FLOAT)

        self.linpos_KP                      = WheeledBase.Parameter(self, POSITIONCONTROL_LINVELKP_ID, FLOAT)
        self.angpos_KP                      = WheeledBase.Parameter(self, POSITIONCONTROL_ANGVELKP_ID, FLOAT)
        self.max_linvel                     = WheeledBase.Parameter(self, POSITIONCONTROL_LINVELMAX_ID, FLOAT)
        self.max_angvel                     = WheeledBase.Parameter(self, POSITIONCONTROL_ANGVELMAX_ID, FLOAT)
        self.linpos_threshold               = WheeledBase.Parameter(self, POSITIONCONTROL_LINPOSTHRESHOLD_ID, FLOAT)
        self.angpos_threshold               = WheeledBase.Parameter(self, POSITIONCONTROL_ANGPOSTHRESHOLD_ID, FLOAT)

        self.lookahead                      = WheeledBase.Parameter(self, PUREPURSUIT_LOOKAHEAD_ID, FLOAT)
        self.lookaheadbis                   = WheeledBase.Parameter(self, PUREPURSUIT_LOOKAHEADBIS_ID, FLOAT)
        self.x                              = 0
        self.y                              = 0
        self.theta                          = 0
        self.previous_measure               = 0
        self.direction = self.NO_DIR
        self.final_angle = 0

        self.publisher_set_velocities=rospy.Publisher(SET_VELOCITIES_OPCODE,Vector3,queue_size=10)
        self.publisher_set_openloop_velocities=rospy.Publisher(SET_OPENLOOP_VELOCITIES_OPCODE,Vector3,queue_size=10)
        self.publisher_set_position=rospy.Publisher(SET_POSITION_OPCODE,Vector3,queue_size=10)
        
        self.publisher_goto_delta=rospy.Publisher(GOTO_DELTA_OPCODE,Vector3,queue_size=10)
        

        self.publisher_start_turnonthespot=rospy.Publisher(START_TURNONTHESPOT_OPCODE,tos_data)
        self.publisher_start_turnonthespot_dir=rospy.Publisher(START_TURNONTHESPOT_DIR_OPCODE,tos_data)

        self.publisher_reset_parameters=rospy.Publisher(RESET_PARAMETERS_OPCODE,String)
        self.publisher_save_parameters=rospy.Publisher(SAVE_PARAMETERS_OPCODE,String)

        self.publisher_add_purepursuit_waypoint=rospy.Publisher(ADD_PUREPURSUIT_WAYPOINT_OPCODE,Vector3,queue_size=10)
        
        self.publisher_reset_purepursuit=rospy.Publisher(RESET_PUREPURSUIT_OPCODE,String,queue_size=10)
        
        self.publisher_start_purepursuit=rospy.Publisher(START_PUREPURSUIT_OPCODE,tos_data)
        
        self.publisher_set_parameter_value=rospy.Publisher(SET_PARAMETER_VALUE_OPCODE,Vector3)
         
        self.codewheel_counter = 0
        rospy.Subscriber(GET_CODEWHEELS_COUNTERS_OPCODE, Vector3, self.callback_codewheels_counter)
        
        self.position = 0
        rospy.Subscriber(GET_POSITION_OPCODE, Vector3, self.callback_position)
        
        self.velocities = 0
        rospy.Subscriber(GET_VELOCITIES_OPCODE, Vector3, self.callback_velocities)
        
        self.velocities_wanted = 0
        rospy.Subscriber(GET_VELOCITIES_WANTED_OPCODE, Vector3, self.callback_velocities_wanted)
        
        self.position_reached=0
        rospy.Subscriber(POSITION_REACHED_OPCODE, Vector3, self.callback_position_reached)
        
        self.parameter=0
        rospy.Subscriber(POSITION_REACHED_OPCODE, Vector3, self.callback_position_reached)

        #GET_PARAMETER_VALUE_OPCODE      = "wheelbase/GET_PARAMETER_VALUE"
        

        self.latch = None
        self.latch_time = None

    def set_parameter_value(self, id, value, valuetype):
        self.publisher_set_parameter_value.publish(Vector3(id,value,valuetype))
        time.sleep(0.01)

    #A REFAIRE
    #def get_parameter_value(self, id, valuetype):
        #output = self.execute(GET_PARAMETER_VALUE_OPCODE, BYTE(id))
        #value = output.read(valuetype)
        #return value

    def get_parameter_value(self, id, valuetype):
        return None

    def set_openloop_velocities(self, left, right):
        self.publisher_set_openloop_velocities.publish(Vector3(left,right,0))


    def callback_codewheels_counter(self,data):
        self.codewheel_counter=data[0:1]


    def get_codewheels_counter(self, **kwargs):
        return self.codewheel_counter[0], self.codewheel_counter[1]

    def set_velocities(self, linear_velocity, angular_velocity):
        self.publisher_set_velocities.publish(Vector3(linear_velocity,angular_velocity,0))

    def purepursuit(self, waypoints, direction='forward', finalangle=None, lookahead=None, lookaheadbis=None, linvelmax=None, angvelmax=None, **kwargs):
        if len(waypoints) < 2:
            raise ValueError('not enough waypoints')
        
        self.publisher_reset_purepursuit.publish("reset")
        for x, y in waypoints:
            vec=Vector3()
            vec.x=x
            vec.y=y
            self.publisher_add_purepursuit_waypoint(vec)
        if lookahead is not None:
            self.set_parameter_value(PUREPURSUIT_LOOKAHEAD_ID, lookahead, FLOAT)
        if lookaheadbis is not None:
            self.set_parameter_value(PUREPURSUIT_LOOKAHEADBIS_ID, lookaheadbis, FLOAT)
        if linvelmax is not None:
            self.set_parameter_value(POSITIONCONTROL_LINVELMAX_ID, linvelmax, FLOAT)
        if angvelmax is not None:
            self.set_parameter_value(POSITIONCONTROL_ANGVELMAX_ID, angvelmax, FLOAT)
        if finalangle is None:
            finalangle = math.atan2(waypoints[-1][1] - waypoints[-2][1], waypoints[-1][0] - waypoints[-2][0])
        self.direction = {'forward':self.FORWARD, 'backward':self.BACKWARD}[direction]
        self.final_angle = finalangle
        data=tos_data()
        data.angle=self.final_angle
        data.modalite={self.NO_DIR:False, self.FORWARD:False, self.BACKWARD:True}[self.direction]
        self.publisher_start_purepursuit(data)


    def start_purepursuit(self):
        data=tos_data()
        data.angle=self.final_angle
        data.modalite={self.NO_DIR:False, self.FORWARD:False, self.BACKWARD:True}[self.direction]
        self.publisher_start_purepursuit(data)

    def turnonthespot(self, theta, direction=None, way='forward'):
        if direction is None:
            data=tos_data()
            data.angle=theta
            data.modalite={'forward':False, 'backward':True}[way]
            self.publisher_start_turnonthespot(data)
        else:
            data=tos_data()
            data.angle=theta
            data.modalite={'clock':False, 'trig':True}[direction]
            self.publisher_start_turnonthespot_dir(data)

    def callback_position_reached(self,data):
        self.position_reached=data[1:2]

    def isarrived(self, **kwargs):
        isarrived, spinurgency = self.position_reached
        if bool(spinurgency):
            raise RuntimeError('spin urgency')
        return bool(isarrived)

    def callback_velocities_wanted(self,data):
        self.velocities_wanted=data[0:1]

    def get_velocities_wanted(self, **kwargs):
        return self.velocities_wanted[0], self.velocities_wanted[1]


    def wait(self, timestep=0.1, timeout=200, command=None, **kwargs):
        init_time = time.time()
        while not self.isarrived(**kwargs):
            time.sleep(timestep)
            if (time.time()-init_time>timeout) and (not command is None):
                print("RESCUE wheeledbase !")
                command()
                time.sleep(timestep)

    def goto_delta(self, x, y):
        vec=Vector3()
        vec.x=x
        vec.y=y
        self.publisher_goto_delta(vec)

    def goto(self, x, y, theta=None, direction=None, finalangle=None, lookahead=None, lookaheadbis=None, linvelmax=None, angvelmax=None, **kwargs):
        # Compute the preferred direction if not set
        if direction is None:
            x0, y0, theta0 = self.get_position()
            if math.cos(math.atan2(y - y0, x - x0) - theta0) >= 0:
                direction = 'forward'
            else:
                direction = 'backward'

        # Go to the setpoint position
        self.purepursuit([self.get_position()[0:2], (x, y)], direction, finalangle, lookahead, lookaheadbis, linvelmax, angvelmax)
        self.wait(**kwargs)

        # Get the setpoint orientation
        if theta is not None:
            self.turnonthespot(theta)
            self.wait(**kwargs)

    def stop(self):
        self.set_openloop_velocities(0, 0)

    def set_position(self, x, y, theta):
        vec=Vector3()
        vec.x=x
        vec.y=y
        vec.z=theta
        self.publisher_set_position.publish(vec)
        

    def reset(self):
        self.set_position(0, 0, 0)

    def callback_position(self,data):
        self.position=data

    def get_position(self, **kwargs):
        self.x, self.y, self.theta = self.position
        self.previous_measure = time.time()
        return self.x, self.y, self.theta

    def get_position_latch(self, **kwargs):
        if self.latch is None or time.time() - self.latch_time > self.LATCH_TIMESTEP:
            self.latch = self.get_position(**kwargs)
            self.latch_time = time.time()
        return self.latch

    def get_position_previous(self, delta):
        if time.time()-self.previous_measure>delta:
            self.get_position()
        return self.x, self.y, self.theta

    def callback_velocities(self,data):
        self.velocities=data[1:2]

    def get_velocities(self, **kwargs):
        linvel, angvel = self.velocities
        return linvel, angvel

    def reset_parameters(self):
        self.publisher_reset_parameters.publish("reset")
        

    def save_parameters(self):
        self.publisher_save_parameters.publish("save")
        
