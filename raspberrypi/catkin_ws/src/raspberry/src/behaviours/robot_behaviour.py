#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import monotonic, sleep
from threading import Thread, Event, current_thread
from logs.log_manager import *
from listeners.end_game_listener import *


class AccessDenied(Exception):
    pass


class RobotBehavior:
    """This class describe the generic beahviour of the robot. How to reach an action point and how to excute the desired action

    Raises:
        TimeoutError: Timeout on communication or action
        AccessDenied: Thread is not allowed to execute on manager
        RuntimeError: Function not override
        RuntimeError: Function not override
        RuntimeError: Function not override
        RuntimeError: Function not override
        RuntimeError: Function not override
    """
    BLUE_SIDE = 0
    YELLOW_SIDE = 1
    UNDEFINED_SIDE = -1

    def __init__(self, manager, *args, timelimit=None, exec_param=Logger.SHOW, log_level=INFO, **kwargs):
        """Initialise all the useful object members

        Args:
            manager (class): The manager proxy
            timelimit (int, optional): The match time limit. Defaults to None.
            exec_param (int, optional): The logger display configuration. Defaults to Logger.SHOW.
            log_level (int, optional): The logger display level. Defaults to INFO.
        """
        self.manager = manager
        self.timelimit = timelimit
        self.whitelist = set()
        self.blacklist = set()
        self.outputs = dict()
        self.stop_event = Event()

        # Keep old manager method
        #self.manager_send = self.manager.send

        # Override manager send method
        #self.manager.send = self.send

        # Init Logger
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

    def perform(self, procedure, args=(), kwargs={}, timelimit=True):
        """This method allow the robot to perform an action. It create one thread for the current action and check if this thread is allow to run

        Args:
            procedure (function): The desired action procedure
            args (tuple, optional): The procedure arguments. Defaults to ().
            kwargs (dict, optional): The procedure kwargs . Defaults to {}.
            timelimit (bool, optional): The match time limit. Defaults to True.

        Returns:
            Thread : Return the created thread
        """
        thread = Thread(args=args, kwargs=kwargs, daemon=True)
        thread_id = id(thread)

        def target(*args, **kwargs):
            try:
                output = procedure(*args, **kwargs)
                self.outputs[thread_id] = output
            except AccessDenied:
                self.outputs[thread_id] = None
            except:
                self.outputs[thread_id] = None
                raise
            finally:
                if thread_id in self.blacklist:
                    self.blacklist.remove(thread_id)
                if thread_id in self.whitelist:
                    self.whitelist.remove(thread_id)

        if not timelimit:
            self.whitelist.add(thread_id)
        thread._target = target
        thread.start()
        return thread

    def interrupt(self, thread):
        """Interrupt the desired thread (Action procedure)

        Args:
            thread (Thead id): The wanted thread
        """
        if thread.is_alive():
            thread_id = id(thread)
            self.blacklist.add(thread_id)

    def get(self, thread, timeout=None):
        """Wait for the current running thread(Action procedure) is end. Return the procedure result after.

        Args:
            thread (Thread id): The current action thread to perform
            timeout (int, optional): The action timeout. Defaults to None.

        Raises:
            TimeoutError: Raise this error when a timeour occur

        Returns:
            return param: the output parameter of the thread
        """
        thread.join(timeout=timeout)
        if thread.is_alive():
            raise TimeoutError('timeout exceeded')
        thread_id = id(thread)
        output = self.outputs[thread_id]
        del self.outputs[thread_id]
        return output

    def send(self, *args, **kwargs):
        """redefine the manager send method in order to only use the proxy when the running thread is authorized

        Raises:
            AccessDenied: When the acces is denied for current thread

        Returns:
            Manager ret code
        """
        thread_id = id(current_thread())
        denyaccess = thread_id in self.blacklist
        if not thread_id in self.whitelist:
            if self.timelimit is not None:
                denyaccess |= (self.get_elapsed_time() > self.timelimit)
            denyaccess |= self.stop_event.is_set()
        if denyaccess:
            raise AccessDenied(thread_id)
        else:
            return self.manager(self, *args, **kwargs)

    def start_preparation(self):
        """This method is called during prepartion phase in order to run the robot IHM and allow the user to setup the robot before a match.
        """
        from managers.buttons_manager import ButtonsManager
        ButtonsManager(self).begin()

    def make_decision(self):
        """This function is called to choose which action to execute. The child robot needs to override this method to choose the decision behavior

        Raises:
            RuntimeError: When the method in not override by the child class
        """
        raise RuntimeError("the 'make_decision' method must be overriden")

    def goto_procedure(self, destination):
        """This function is called to choose how to reach an action point. The child robot needs to override this method to choose the moving behavior

        Args:
            destination (tuple): The robot destionation coordinates x,y,theta

        Raises:
            RuntimeError: When the method in not override by the child class
        """
        raise RuntimeError("the 'goto_procedure' method must be overriden")

    def set_side(self, side):
        """This function is called to choose the robot side. The child robot needs to override this method to choose how to attribute a side

        Args:
            side (int): the side color

        Raises:
            RuntimeError: When the method in not override by the child class
        """
        raise RuntimeError("the 'set_side' method must be overriden")

    def set_position(self):
        """This function is called to setup the starting position. The child robot needs to override this method to apply the stating position

        Raises:
            RuntimeError: When the method in not override by the child class
        """
        raise RuntimeError("the 'set_position' method must be overriden")

    def positioning(self):
        """Optionnal positioning method to do a small move after setting up the start position
        """
        pass

    def start_procedure(self):
        """Optionnal function running when the robot start its match. Usually used tu put the actuators to its default position
        """
        pass

    def stop_procedure(self):
        """Optionnal function running at the end of match. Usually used to check if the funny action is end
        """
        pass

    def start(self):
        """This method is the core of the robot. It allow the robot to go to each action and reach all action points
        """
        self.starttime = monotonic()
        self.stop_event.clear()
        self.logger(INFO, 'Start Behaviour')
        try:
            start = self.perform(self.start_procedure, timelimit=False)
            while (self.timelimit is None or self.get_elapsed_time() < self.timelimit) and not self.stop_event.is_set():
                decision = self.make_decision()
                procedure, args, kwargs, (location, thresholds) = decision
                if procedure is None:
                    self.logger(INFO, 'No decision')
                    sleep(1)
                    continue
                if location is not None:
                    if location[2] is not None:
                        self.logger(
                            INFO, 'Goto: ({0[0]:.0f}, {0[1]:.0f}, {0[2]:.2f})'.format(location))
                    else:
                        self.logger(
                            INFO, 'Goto: ({0[0]:.0f}, {0[1]:.0f})'.format(location))
                    goto = self.perform(self.goto_procedure,
                                        args=(location, thresholds))
                    success = self.get(goto)
                else:
                    success = True
                if success:
                    self.logger(INFO, "Perform Action")
                    action = self.perform(procedure, args=args, kwargs=kwargs)
                    self.get(action)
                else:
                    self.logger(WARNING, 'Goto failed')
        except:
            self.whitelist.clear()
            raise
        finally:
            self.stop()
            self.get(start)
            self.whitelist.add(id(current_thread()))
            self.stop_procedure()

    def stop(self):
        """Stop the robot
        """
        self.logger(INFO, 'Stop match')
        self.stop_event.set()

    def get_elapsed_time(self):
        """Get the time elapsed from the start of match

        Returns:
            long: the elapsed time
        """
        if hasattr(self, 'starttime'):
            return monotonic() - self.starttime
        else:
            return 0


if __name__ == "__main__":
    from math import pi

    from setups.setup_serialtalks import *
    from setups.setup_wheeledbase import *
    from behaviours.action.action import *

    class TakeCup(Action):
        def __init__(self, idx):
            self.idx = idx
            self.actionpoint = (555, 666)  # geogebra.get('Point name')
            self.orientation = pi
            self.actionpoint_precision = 10

        def procedure(self, robot):
            print(robot.__class__.__name__)
            print('take : ', self.idx)
            sleep(1)

    class Robot(RobotBehavior):
        def __init__(self, manager, *args, timelimit=None, **kwargs):
            RobotBehavior.__init__(self, manager, *args,
                                   timelimit=timelimit, **kwargs)

            take1 = TakeCup(1)
            take2 = TakeCup(2)
            take3 = TakeCup(3)
            take4 = TakeCup(4)
            take5 = TakeCup(5)

            self.automate = [
                take1,
                take2,
                take3,
                take4,
                take5
            ]

            self.automatestep = 0

        def make_decision(self):
            if(self.automatestep < len(self.automate)):
                action = self.automate[self.automatestep]
            else:
                return None, (self,), {}, (None, None)
                self.stop_event.set()

            return action.procedure, (self,), {}, (action.actionpoint + (action.orientation,), (action.actionpoint_precision, None))

        def goto_procedure(self, destination, thresholds=(None, None)):
            self.automatestep += 1
            sleep(1)
            return True

    rb = Robot(manager, timelimit=20)

    rb.start()
