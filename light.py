# Pour les timers os.alarm (Check TD sur les signaux)
# Pour les threads, threading.Timer
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import time
from queue import Queue
import signal
class TraficLight:
    def __init__(self):
        self.light=0b1001
        class QueueManager(BaseManager): pass
        QueueManager.register('get_queue')
        m = QueueManager(address=('localhost', 5002))
        m.connect()
        self.queue = m.get_queue()
        self.timerSwitch=True
        self.timer_light(None,None)
        
    def switch_light(self):
        self.light = self.light ^ 0b1111
        self.queue.put(self.light)
    def timer_light(self,a, b):
        if self.timerSwitch:
            self.switch_light()
            print(bin(self.light))
            signal.signal(signal.SIGALRM, self.timer_light)
            signal.alarm(5)

def trafic_light_gen():
    t=TraficLight()
    
        
if __name__ == "__main__":
    trafic_light_gen()