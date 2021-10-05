#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event
from time import monotonic, sleep
from math import hypot

from common.sync_flag_signal import Signal, Flag

class EndGameListener(Thread):

    # End game actions
    END_GAME_ACTION = 0
    FUNNY_ACTION    = 1
    HARBOUR_ACTION  = 2
    # Add new end game action here

    def __init__(self, match_time = 100,  timestep = 0.1):
        Thread.__init__(self)
        self.daemon = True

        # End Game action list
        self.end_game_action_list = [self.END_GAME_ACTION, self.FUNNY_ACTION, self.HARBOUR_ACTION]

        for action in self.end_game_action_list:
            self.__setattr__("signal"+str(action) , Signal())
            self.__setattr__("timeout"+str(action) , match_time)
            self.__setattr__("event"+str(action) , Event())

        # Timestep
        self.timestep = timestep

        # Stopping eventc

        self.stop = Event()

    def bind(self, idx, func, timeout=100):
        self.__setattr__("flag"+str(idx), Flag(func))
        self.__getattribute__("flag"+str(idx)).bind(self.__getattribute__("signal"+str(idx)))
        self.__setattr__("timeout"+str(idx), timeout)

    def run(self):
        start_time = monotonic()
        while not self.stop.is_set():
            # Handle end game actions
            for action in self.end_game_action_list:
                if monotonic() - start_time >= self.__getattribute__("timeout"+str(action)):
                    if not self.__getattribute__("event"+str(action)).is_set():
                        self.__getattribute__("signal"+str(action)).ping()
                        self.__getattribute__("event"+str(action)).set()

            sleep(self.timestep)

if __name__ == "__main__":
    endGame = EndGameListener()
    start_time = monotonic()

    def stop_match():
        print(monotonic() - start_time)
        print("stop !!")

    def funny():
        print(monotonic() - start_time)
        print("funny !!")

    def harbour():
        print(monotonic() - start_time)
        print("harbour !!")

    endGame.bind(EndGameListener.END_GAME_ACTION, stop_match)
    endGame.bind(EndGameListener.FUNNY_ACTION, funny, timeout=20)
    endGame.bind(EndGameListener.HARBOUR_ACTION, harbour, timeout=65)

    endGame.start()

    input()