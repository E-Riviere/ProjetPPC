# Pour les timers os.alarm (Check TD sur les signaux)
# Pour les threads, threading.Timer

import signal
import shared_memory_process
import time
import os
class TraficLight:
    def __init__(self):
        data_process=shared_memory_process.shared_memory_manager('light')
        print(data_process)
        self.light=0b1001
        self.timerSwitch=True
        self.name_pipe_path = "priority_trafic_pipe"
        self.timer_light(None,None)
        self.pid_coord=int([i for i in data_process if i[0]=='coordinator'][0][1])
        signal.signal(signal.SIGALRM, self.timer_light)
        signal.signal(signal.SIGUSR1, self.vehicule_prio_handler)
        signal.signal(signal.SIGUSR2, self.normal_behavior_handler)

    def switch_light(self):
        self.light = self.light ^ 0b1111
    def timer_light(self,a, b):
        if self.timerSwitch:
            self.switch_light()
            print(bin(self.light))
            signal.alarm(5)
    def vehicule_prio_handler(self,a,b):
        self.timerSwitch=False
        with open(self.name_pipe_path, "r") as pipe:
            self.light=int(pipe.read())
            #self.light =int(pipe.read().decode())
            print("Pinpon")
            print(bin(self.light))
            os.kill(self.pid_coord, signal.SIGUSR1)
            
        
    def normal_behavior_handler(self, a,b):
        print("reset normal")
        self.light = 0b0110 if self.light & 0b0110 == 0 else 0b1001
        self.timerSwitch = True
        self.timer_light(None, None)
    

def trafic_light_gen():
    t=TraficLight()
    

    
if __name__ == "__main__":
    trafic_light_gen()
    
while True:
    #Garder le programme en vie pour les changements de lumière avec Alarm
    time.sleep(1)