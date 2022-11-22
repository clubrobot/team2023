#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread, Event, RLock
from time import sleep
from logs.log_manager import *
from setups.setup_robot_name import *
import sys

from common.tcptalks import TCPTalksServer, TCPTalks

# La position
# Des mutex
_BEACON_PORT = 25568
_BORNIBUS_ID = 1
_R128_ID = 2
_EYE_ID = 3

_NO_SIDE     = 0
_BLUE_SIDE   = 1
_YELLOW_SIDE = 2

_GET_RESSOURCE_OPCODE = 0x11
_RELEASE_RESSOURCE_OPCODE = 0x30
_GET_POS_OPCODE = 0x10
_GET_OTHER_OPCODE = 0x20
_PING_OPCODE = 0x40
_IS_OK_OPCODE = 0x50
_RESET_OPCODE = 0x60
_GET_OPPONENTS_POS_OPCODE = 0x70
_GET_SIDE_OPCODE = 0x80
_SET_SIDE_OPCODE = 0x81
_GET_EYE_FINAL_ORIENTATION_OPCODE = 0x82


class ClientGS(TCPTalks):
    """The Global sync client is used to interconnect robots or beacon using TCPTalks protocol

    Args:
        TCPTalks (class): The TCPTalks client class
    """
    def __init__(self, ID, ip="192.168.12.1", port=_BEACON_PORT):
        """Initialize the client with its id and ip,port. The id is the robot or beacon id (ex: _BORNIBUS_ID)

        Args:
            ID (int): Robot or beacon id
            ip (str, optional): The server ip. Defaults to "192.168.12.1".
            port (int, optional): The server port. Defaults to _BEACON_PORT.
        """
        TCPTalks.__init__(self, ip=ip, port=port, id=ID)
        self.logger = LogManager().getlogger("ClientGS", Logger.WRITE, level_disp=INFO)
        self.bind(_PING_OPCODE, self._refresh)
        self.bind(_GET_POS_OPCODE, self._get_my_pos)
        self.bind(_GET_EYE_FINAL_ORIENTATION_OPCODE, self._get_my_final_orientation)

    def reset_ressources(self):
        """Reset all server ressources
        """
        self.send(_RESET_OPCODE)

    def get_ressource(self, name):
        """Distributed mutex to lock resources on the server (ex: access to a shared action)

        Args:
            name (string): The ressource name

        Returns:
            Bool: Exist or not
        """
        try:
            return self.execute(_GET_RESSOURCE_OPCODE, self.id, name)
        except:
            return False

    def release_ressource(self, name):
        """Distributed mutex to unlock resources on the server (ex: access to a shared action)

        Args:
            name (string): The ressource name
        """
        try:
            self.send(_RELEASE_RESSOURCE_OPCODE, self.id, name)
        except:
            try:
                self.send(_RELEASE_RESSOURCE_OPCODE, self.id, name)
            except:
                pass

    def is_active(self):
        """Check if the client and server is connected

        Returns:
            bool : Connected or not
        """
        if not self.is_connected:
            return False
        try:
            return self.execute(_IS_OK_OPCODE, self.id, timeout=1)
        except:
            return False

    def _refresh(self):
        """Refresh

        Returns:
            Bool : true
        """
        return True

    def get_brother_pos(self):
        """Get the pos of our brother robot in order to avoid it

        Returns:
            tuple: The brother x, y, theta position
        """
        other = _BORNIBUS_ID if self.id == _R128_ID else _R128_ID
        return self.execute(_GET_OTHER_OPCODE, other)

    def get_opponents_pos(self):
        """Get the opponent pos from the supervior beacon that can detect oppoenets whith the ArUco tags

        Returns:
            list of tuple: The the all opponents [(x, y, theta), (x, y, theta)] position
        """
        return self.execute(_GET_OPPONENTS_POS_OPCODE)

    def _get_my_pos(self):
        """Internal method to give my pos to my brother, by default, return my pos outise of the game area, it can be redefined by the Robot Client

        Returns:
            tuple: my x, y, theta position
        """
        return (-1000, -1000+self.id)

    def get_side(self):
        """Get the side configured on the robot

        Returns:
            int : Side color
        """
        return self.execute(_GET_SIDE_OPCODE)

    def _get_my_final_orientation(self):
        """Used internally to return the wheatervane orientation, redifined by EY

        Returns:
            None
        """
        return None

    def get_final_orientation(self):
        """Get final wheathervane orientation

        Returns:
            int: the orientation
        """
        return self.execute(_GET_EYE_FINAL_ORIENTATION_OPCODE)


class ServerGS(TCPTalksServer):
    """The global sync server used to communicate between robots and beacon over TCPTalks

    Args:
        TCPTalksServer (Class): The TCPTalks server
    """
    def __init__(self):
        TCPTalksServer.__init__(self, _BEACON_PORT)
        self.ressources = dict()
        self.mutex = RLock()
        self.logger = LogManager().getlogger("ServerGS", Logger.WRITE, level_disp=INFO)
        self.bornibus_id = -1
        self.r128_id = -1
        self.bind(_GET_OTHER_OPCODE, self.get_pos)
        self.bind(_GET_RESSOURCE_OPCODE, self.get_ressource)
        self.bind(_RELEASE_RESSOURCE_OPCODE, self.release_ressource)
        self.bind(_IS_OK_OPCODE, self._is_ok)
        self.bind(_RESET_OPCODE, self._reset)
        self.bind(_GET_OPPONENTS_POS_OPCODE, self.get_opponents_pos)
        self.bind(_GET_SIDE_OPCODE, self.get_side)
        self.bind(_GET_EYE_FINAL_ORIENTATION_OPCODE, self._get_final_orientation)

        self.side = _NO_SIDE

        self.logger(INFO, "ServerGS succefully initialised")

    def run(self):
        """The server main loop to handle client connection
        """
        while True:
            try:
                while not self.full():
                    self.connect(timeout=100)
                self.sleep_until_one_disconnected()

            except KeyboardInterrupt:
                break
            except Exception as e:
                sys.stderr.write('{}: {}\n'.format(type(e).__name__, e))
                continue

    def _reset(self):
        """Called when a ressources reset is requested by a client
        """
        for key in list(self.ressources.keys()):
            self.ressources[key] = -1

    def _is_ok(self, idx):
        """Check if the client is joinable

        Args:
            idx (int): Client id

        Returns:
            bool: Yes or no
        """
        if _BORNIBUS_ID in list(self.client.keys()) and _R128_ID in list(self.client.keys()):
            try:
                if idx == _BORNIBUS_ID:
                    self.execute(_PING_OPCODE, id=_R128_ID)
                else:
                    self.execute(_PING_OPCODE, id=_BORNIBUS_ID)
                return True
            except:
                return False
        else:
            return False

    def get_pos(self, idx):
        """Return the pos of the requested robot, return outise of playing area if the robot doesn't exist

        Args:
            idx (int): the Robto id

        Returns:
            tuple : The position of the robot
        """
        if not idx in list(self.client.keys()):
            return (-1000, -1000)

        pos = self.execute(_GET_POS_OPCODE, id=idx)
        return pos

    def get_opponents_pos(self):
        """Return the position of the opponents, by default outisde of the playing area, it is redified inised supervisor server

        Returns:
            [type]: [description]
        """
        return [(-1000, -1000),(-1000, -1000)]

    def get_ressource(self, idx, name):
        """Lock a shared mutex with the other robot

        Args:
            idx (int): The robot id
            name (string): The ressource name

        Raises:
            RuntimeError: execution error

        Returns:
            bool: True or false
        """
        if not self.mutex.acquire(timeout=0.5):
            return False

        self.logger(INFO, "Ressource {} asking by {}".format(name, idx))
        if not name in list(self.ressources.keys()):
            self.logger(ERROR, "Unknown ressource !")
            self.mutex.release()
            raise RuntimeError("Unknown ressource !")

        if self.ressources[name] != -1 and self.ressources[name] != idx:
            try:
                self.execute(_PING_OPCODE, id=self.ressources[name])
            except (ConnectionError, TimeoutError, KeyError):
                self.ressources[name] = idx
                self.mutex.release()
                return True
            self.mutex.release()
            self.logger(WARNING, "Rejected")
            return False
        else:
            self.logger(INFO, "Mutex {} attributed to a {}".format(name, idx))
            self.ressources[name] = idx
            self.mutex.release()
            return True

    def release_ressource(self, idx, name):
        """Unlock a shared mutex with the other robot

        Args:
            idx (int): The robot id
            name (string): The ressource name

        Raises:
            RuntimeError: execution error
        """
        if not self.mutex.acquire(timeout=0.5):
            return
        self.logger(INFO, "Release mutex {} by {}".format(name, idx))
        if not name in list(self.ressources.keys()):
            self.mutex.release()

        if self.ressources[name] != idx:
            self.mutex.release()
            return
        else:
            self.ressources[name] = -1
            self.mutex.release()
            return

    def set_side(self, side):
        """Set the side from the robot configuration

        Args:
            side (int): The color side
        """
        self.side = side

    def get_side(self):
        """Get the side configured on robot

        Returns:
            int: Color side
        """
        return self.side

    def _get_final_orientation(self):
        """Return the final orientation come from the eyeClient

        Returns:
            int: The final wheathervane orientation
        """
        if not _EYE_ID in list(self.client.keys()):
            return None

        orientation = self.execute(_GET_EYE_FINAL_ORIENTATION_OPCODE, id=_EYE_ID)
        return orientation