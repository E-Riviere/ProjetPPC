import random
import socket
import signal
import os
import time
from multiprocessing import shared_memory
import shared_memory_process
import sysv_ipc

HOST = "localhost"
PORT = 8080

key = 128
coord = None
class Coordinator:

    def __init__(self):
        signal.signal(signal.SIGUSR1, lambda a,b: None)
        self.data_process = shared_memory_process.shared_memory_manager('coordinator')
        self.existing_shm = shared_memory.SharedMemory(name="trafficLightState")
        signal.signal(signal.SIGUSR1, lambda a, b: sig_usr1_handler(self.light_pid,self.existing_shm))

        self.data = [["R","R","R","R"],"","","","","An action"]
        self.voiture1 = ""
        self.voiture2 = ""
        self.message = ""
        self.north = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
        self.south = sysv_ipc.MessageQueue(key + 1, sysv_ipc.IPC_CREAT)
        self.west = sysv_ipc.MessageQueue(key + 2, sysv_ipc.IPC_CREAT)
        self.east = sysv_ipc.MessageQueue(key + 3, sysv_ipc.IPC_CREAT)
        self.light_pid=int([i for i in self.data_process if i[0]=='light'][0][1])
        self.conn = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)

    def receive_normal_queue(self,queue):
        try:
            message, t = queue.receive(type=1,block=False)
            message = message.decode()
        except sysv_ipc.BusyError:
            message = None
        return message
    
    def receive_priority_queue(self,queue):
        self.message = None
        while self.message == None:
            try:
                self.message, t = queue.receive(type=2,block=False)
                self.message = self.message.decode()
            except sysv_ipc.BusyError:
                self.message = None
        return self.message

    def mainLoop(self):
        self.data = [["R","R","R","R"],"","","","",""]
        while True:
            light_changed = False
            old_light = self.data[0]

            try:
                if self.existing_shm.buf:
                    if self.existing_shm.buf[0] == 0b0110:
                        
                        self.voiture1 = self.receive_normal_queue(self.west)
                        self.voiture2 = self.receive_normal_queue(self.east)
                        self.data = [["R","V","V","R"],"",self.voiture1,self.voiture2,"","No action"]
                        light_changed = old_light != self.data[0]
                    
                    elif self.existing_shm.buf[0] == 0b1001:
                        light_changed = old_light == self.data[0]
                        self.voiture1 = self.receive_normal_queue(self.north)
                        self.voiture2 = self.receive_normal_queue(self.south)
                        self.data = [["V","R","R","V"],self.voiture1,"","",self.voiture2,"No action"]
                        light_changed = old_light != self.data[0]
                
                if self.conn == None:
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.conn, addr = self.server_socket.accept()
                    print(f"Connection from {addr}")
                else:
                    if self.voiture1 != None or self.voiture2 != None or light_changed and self.data:
                        print(self.data)

                        self.data[5] = "Normal traffic"
                        self.strdata = str(self.data)
                        try:
                            self.conn.send(self.strdata.encode())
                        except Exception as e:
                            print("Error", e)
                            pass


                    try:
                        data_recv = self.conn.recv(1024,socket.MSG_DONTWAIT)
                        if data_recv == b"exit":
                            self.clearMemory()
                        elif data_recv == None:
                            self.conn.close()
                            self.conn = None
                            print("Connection closed")
                    except:
                        pass

                if self.voiture1 or self.voiture2:
                    time.sleep(random.randint(1,2))
            except Exception as e:
                print(e)
                self.clearMemory()
                break
            except KeyboardInterrupt:
                print("Keyboard interrupt")
                self.clearMemory()
                break

    def clearMemory(self):
            
            self.existing_shm.close()
            self.existing_shm.unlink()
            self.server_socket.close()
            self.client_socket.close()
            if self.conn != None:
                self.conn.close()
            print("Server closed")
            try:
                self.north.remove()
                self.south.remove()
                self.west.remove()
                self.east.remove()
            except Exception as e:
                print(e)
                pass
            exit()
    
def sig_usr1_handler(pid,shm):

    if shm.buf[0] in [0b1000,0b0100, 0b0010, 0b0001] and coord != None:
        message = None
        coord.data = [["R","R","R","R"],"","","","",""]
        while message==None:
            source = None
            if shm.buf[0] == 0b1000:
                message = coord.receive_priority_queue(coord.north)
                source = "North"
                coord.data[0] = ["V","R","R","R"]
                coord.data[1] = message
            elif shm.buf[0] == 0b0100:
                message = coord.receive_priority_queue(coord.west)
                source = "West"
                coord.data[0] = ["R","V","R","R"]
                coord.data[2] = message
            elif shm.buf[0] == 0b0010:
                message = coord.receive_priority_queue(coord.east)
                source = "East"
                coord.data[0] = ["R","R","V","R"]
                coord.data[3] = message
            elif shm.buf[0] == 0b0001:
                message = coord.receive_priority_queue(coord.south)
                source = "South"
                coord.data[0] = ["R","R","R","V"]
                coord.data[4] = message

        if message != None:
            coord.data[5] = "Priority vehicule from" + source
            if coord.conn != None:
                coord.strdata = str(coord.data)
                try:
                    coord.conn.send(coord.strdata.encode())
                except Exception as e:
                    print("Error", e)
                    pass
            time.sleep(random.randint(1,2))
            os.kill(pid, signal.SIGUSR2)
            coord.mainLoop()

    
    
    





if __name__ == "__main__":
    coord = Coordinator()
    coord.mainLoop()
    coord.clearMemory()




                    
            