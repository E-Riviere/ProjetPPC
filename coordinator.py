import random
import socket
import signal
import os
import time
from multiprocessing import shared_memory
import shared_memory_process
import sysv_ipc

AVG_TIME_TO_PASS = 3 
HOST = "localhost"
PORT = 8080

key = 128
coord = None
class Coordinator:

    def __init__(self):
        signal.signal(signal.SIGUSR1, lambda a,b: None)
        self.data_process = shared_memory_process.shared_memory_manager('coordinator')
        self.existing_shm = shared_memory.SharedMemory(name="trafficLightState")
        signal.signal(signal.SIGUSR1, lambda a, b: sig_usr1_handler(self.light_pid, self.existing_shm))
        signal.signal(signal.SIGINT, sig_int_handler)
        self.pid = os.getpid()
        self.data = [["R","R","R","R"],"","","","","An action"]
        self.voitureN = ""
        self.voitureW = ""
        self.voitureS = ""
        self.voitureE = ""
        self.voitureNState = "Passing"
        self.voitureWState = "Passing"
        self.voitureSState = "Passing"
        self.voitureEState = "Passing"
        self.message = ""
        self.north = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
        self.south = sysv_ipc.MessageQueue(key + 1, sysv_ipc.IPC_CREAT)
        self.west = sysv_ipc.MessageQueue(key + 2, sysv_ipc.IPC_CREAT)
        self.east = sysv_ipc.MessageQueue(key + 3, sysv_ipc.IPC_CREAT)
        self.light_pid = int([i for i in self.data_process if i[0] == 'light'][0][1])
        self.conn = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        self.priority = False

    def receive_normal_queue(self, queue):
        try:
            message, t = queue.receive(type=1, block=False)
            message = message.decode()
        except sysv_ipc.BusyError:
            message = None
        return message

    def receive_priority_queue(self, queue):
        self.message = None
        while self.message == None:
            try:
                self.message, t = queue.receive(type=2, block=False)
                self.message = self.message.decode()
            except sysv_ipc.BusyError:
                self.message = None
        return self.message

    def mainLoop(self):
        self.data = [["R","R","R","R"],"","","","",""]
        self.light_changed = False
        if self.conn == None:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn, addr = self.server_socket.accept()
            except OSError:
                pass
        while True:
            self.old_light = self.data[0]
            try:
                if self.existing_shm.buf:
                    if self.existing_shm.buf[0] == 0b0110:
                        if self.voitureWState != "Waiting":
                            self.voitureW = self.receive_normal_queue(self.west)
                        if self.voitureEState != "Waiting":
                            self.voitureE = self.receive_normal_queue(self.east)
                        if self.voitureW and self.voitureE:
                            if self.voitureW.split(",")[0] == "North" and self.voitureE.split(",")[0] != "South":
                                self.voitureWState = "Waiting"
                            else:
                                self.voitureWState = "Passing"
                            if self.voitureE.split(",")[0] == "South" and self.voitureW.split(",")[0] != "North":
                                self.voitureEState = "Waiting"
                            else:
                                self.voitureEState = "Passing"
                        else:
                            self.voitureWState = "Passing"
                            self.voitureEState = "Passing"
                        self.data = [["R","V","V","R"], "", str(self.voitureW) + " is " + self.voitureWState, str(self.voitureE) + " is " + self.voitureEState, "", ""]
                        

                    elif self.existing_shm.buf[0] == 0b1001:
                        if self.voitureNState != "Waiting":
                            self.voitureN = self.receive_normal_queue(self.north)
                        if self.voitureSState != "Waiting":
                            self.voitureS = self.receive_normal_queue(self.south)
                        if self.voitureN and self.voitureS:
                            if self.voitureN.split(",")[0] == "East" and self.voitureS.split(",")[0] != "West":
                                self.voitureNState = "Waiting"
                                print("Waiting")
                            else:
                                self.voitureNState = "Passing"
                            if self.voitureS.split(",")[0] == "West" and self.voitureN.split(",")[0] != "East":
                                self.voitureSState = "Waiting"
                                print("Waiting")
                            else:
                                self.voitureSState = "Passing"
                        else:
                            self.voitureNState = "Passing"
                            self.voitureSState = "Passing"
                        self.data = [["V","R","R","V"], str(self.voitureN) + " is " + self.voitureNState, "", "", str(self.voitureS) + " is " + self.voitureSState, ""]
                
                self.light_changed = self.old_light != self.data[0]
                if self.light_changed :
                    print(self.old_light, self.data[0])
                if self.conn == None:
                    pass
                else:
                    if (((self.voitureN != None or self.voitureS != None) and self.data[0] ==["V","R","R","V"]) or ((self.voitureW != None or self.voitureE != None) and self.data[0] ==["R","V","V","R"]) or self.light_changed):
                        self.data[5] = "Normal traffic"
                        self.strdata = str(self.data)
                        try:
                            print("send " , self.strdata,self.old_light )
                            self.conn.send(self.strdata.encode())
                            self.light_changed = False
                        except Exception as e:
                            pass
                    data_recv = None
                    try:
                        data_recv = self.conn.recv(1024, socket.MSG_DONTWAIT)
                    except:
                        pass
                    if data_recv == b"exit":
                        self.conn.close()
                        print("killing")
                        os.kill(self.pid, signal.SIGINT)
                        self.conn = None
                if (self.voitureN or self.voitureS) and self.data[0] ==["V","R","R","V"] or ((self.voitureW  or self.voitureE) and self.data[0] ==["R","V","V","R"]):
                    time.sleep(random.randint(AVG_TIME_TO_PASS - AVG_TIME_TO_PASS // 5, AVG_TIME_TO_PASS + AVG_TIME_TO_PASS // 5))
                if self.voitureE is None and self.voitureN is None and self.voitureS is None and self.voitureW is None:
                    try:
                        message, t = self.north.receive(type=3, block=False)
                        message = message.decode()
                    except sysv_ipc.BusyError:
                        message = None
                    if message != None:
                        os.kill(self.pid,signal.SIGINT)
        
                

            except TypeError:
                pass
            


    def clearMemory(self):
        try:
            self.existing_shm.close()
        except:
            pass
        print("shared memory unlinked")
        self.server_socket.close()
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

def sig_usr1_handler(pid, shm):
    coord.priority = True
    if coord.priority:
        if coord.existing_shm.buf[0] in [0b1000, 0b0100, 0b0010, 0b0001] and coord != None:
            message = None
            coord.data = [["R","R","R","R"],"","","","",""]
            while message == None:
                source = None
                if coord.existing_shm.buf[0] == 0b1000:
                    message = coord.receive_priority_queue(coord.north)
                    source = "North"
                    coord.data[0] = ["V","R","R","R"]
                    coord.data[1] = message
                elif coord.existing_shm.buf[0] == 0b0100:
                    message = coord.receive_priority_queue(coord.west)
                    source = "West"
                    coord.data[0] = ["R","V","R","R"]
                    coord.data[2] = message
                elif coord.existing_shm.buf[0] == 0b0010:
                    message = coord.receive_priority_queue(coord.east)
                    source = "East"
                    coord.data[0] = ["R","R","V","R"]
                    coord.data[3] = message
                elif coord.existing_shm.buf[0] == 0b0001:
                    message = coord.receive_priority_queue(coord.south)
                    source = "South"
                    coord.data[0] = ["R","R","R","V"]
                    coord.data[4] = message

            if message != None:
                coord.data[5] = "Priority vehicule from " + source
                if coord.conn != None:
                    coord.strdata = str(coord.data)
                    try:
                        coord.conn.send(coord.strdata.encode())
                    except Exception as e:
                        pass
                time.sleep(random.randint(AVG_TIME_TO_PASS - AVG_TIME_TO_PASS // 5, AVG_TIME_TO_PASS + AVG_TIME_TO_PASS // 5))
                os.kill(coord.light_pid, signal.SIGUSR2)
    


def sig_int_handler(a, b):
    time.sleep(1)
    print("rneznfior")
    coord.north.send("".encode(),type = 4)
    message = None
    while message == None:
        try:
            message, t = coord.north.receive(type=5, block=False)
            message = message.decode()
        except sysv_ipc.BusyError:
            message = None
    
    coord.existing_shm.close()
    time.sleep(1)
    print("killed mq and gen")
    coord.clearMemory()
    os.kill(coord.light_pid, signal.SIGINT)
    print("killed light")
    raise KeyboardInterrupt()

if __name__ == "__main__":
    coord = Coordinator()
    try:
        coord.mainLoop()
    except Exception as e:
        print(e) 
    