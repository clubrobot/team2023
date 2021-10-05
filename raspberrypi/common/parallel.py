import threading as th
from logs.log_manager import LogManager, DEBUG, INFO, ERROR,CRITICAL
import random
import string
import sys 
import traceback
from common.metaclass import Final

def _randomString(stringLength=4):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class Thread(th.Thread, metaclass=Final):
    """ 
        A custom Thread implementation that use log library in order to catch every crash errors.
        It's prohibited to inherit this class because the run overriting destroy the error catching.
    """ 

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, log=True, daemon=None):
        """
        This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number. This name is used on the log writing.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        th.Thread.__init__(self, group=group, target=target, name=name,
                           args=args, kwargs=kwargs, daemon=daemon)

        self.logger = LogManager().getlogger("Threading", LogManager.BOTH, INFO) if log else None

        if name is None:
            self.name = "thread-"+_randomString(4)
        else:
            self.name = "thread-"+name


    def start(self):
        """
        Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        self.logger(INFO, self.name, "start")
        th.Thread.start(self)


    def run(self):
        """
        Method representing the thread's activity.

        DO NOT OVERRIDE THIS METHOD

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            th.Thread.run(self)
        except (Exception, TypeError):
            etype, value, tb = sys.exc_info()
            self.logger(CRITICAL,self.name,"Error on thread !!", "\n", error=''.join(traceback.format_list(traceback.extract_tb(tb))),type= etype.__name__, value=str(value))

    def join(self, timeout=None):
        """
        Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        isAlive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        """
        self.logger(DEBUG, self.name, "join", timeout=timeout) 
        return th.Thread.join(self,timeout=timeout)

    def is_alive(self):
        """
        Return whether the thread is alive.

        This method returns True just before the run() method starts until just
        after the run() method terminates. The module function enumerate()
        returns a list of all alive threads.

        """
        self.logger(DEBUG, self.name, "is_alive")
        return th.Thread.is_alive(self)

    def isDaemon(self):
        """
            Return if this thread is acctualy a deamond one.
        """
        self.logger(DEBUG, self.name, "isDaemon")
        return th.Thread.isDaemon(self)

    def setDaemon(self, daemonic):
        """
            Set deamon status.
        """
        self.logger(DEBUG, self.name, "setDaemon")
        return th.Thread.setDaemon(self, daemonic)

    def getName(self):
        """
            Basic name getter.
        """
        self.logger(DEBUG, self.name, "getName")
        return th.Thread.getName(self)

    def setName(self, name):
        """
            Basic name setter.
        """
        self.logger(DEBUG, self.name, "setName")     
        return th.Thread(name)



if __name__ == "__main__":
    import time 

    def lol():
        time.sleep(1)
        1/0

    a = LogManager()
    a.start()
    b = Thread(target=lol)
    b.start()
    b.join()
    time.sleep(3)
    a.stop()
    
    class B(Thread):
        pass
