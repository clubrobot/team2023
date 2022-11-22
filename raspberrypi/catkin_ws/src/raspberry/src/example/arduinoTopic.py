from daughter_cards.arduino import ArduinoLocal, TopicHandler, INT
from common.components import Manager


class Test(ArduinoLocal):
    def __init__(self,  port):
        ArduinoLocal.__init__(self,  port)
        self.addTopic(0x1, self.counter_handler, "counter", 1000)
        self.i = 0

    @TopicHandler(INT)
    def counter_handler(self, i):
        self.i = i



if __name__ == "__main__":
    #serv = Manager()
    #serv.connect()
    a = Test("/dev/arduino/wheeledbase")
    a.connect()
    #a.subscribeCounter()
