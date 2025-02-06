import sysv_ipc
import time
import random
import shared_memory_process
import os
import signal
first_key = 128

north = sysv_ipc.MessageQueue(first_key, sysv_ipc.IPC_CREAT)
south = sysv_ipc.MessageQueue(first_key + 1, sysv_ipc.IPC_CREAT)
west = sysv_ipc.MessageQueue(first_key + 2, sysv_ipc.IPC_CREAT)
east = sysv_ipc.MessageQueue(first_key + 3, sysv_ipc.IPC_CREAT)
def del_pipe(path):
    os.remove(path)
    raise KeyboardInterrupt()


def gen_prio_traffic():
    voiture = ""
    i = 0
    pipe_path = "priority_trafic_pipe"
    os.mkfifo(pipe_path)
    data_process=shared_memory_process.shared_memory_manager('priority_traffic_gen')
    signal.signal(signal.SIGINT, lambda a, b: del_pipe(pipe_path))
    light_pid=int([i for i in data_process if i[0]=='light'][0][1])
    while True:
        
        time.sleep(random.randint(5, 15))
        direction = ["South", "East", "West", "North"]
        n_source=random.randint(0, 3)
        source = direction[n_source]
        direction.remove(source)
        destination = direction[random.randint(0, 2)]
        voiture = f"Car{i}"
        message = f"{destination},{voiture}"
        print(source+ ',' + message)
        message = message.encode()
        if source == "North":
            north.send(message, type=2)
            
        elif source == "South":
            south.send(message, type=2)
        elif source == "West":
            west.send(message, type=2)
        else:
            east.send(message, type=2)

        i += 1

        try:
            message, t = north.receive(type=4, block=False)
            message = message.decode()
        except sysv_ipc.BusyError:
            message = None
        if message != None:
            north.send("".encode(),type=5)
            os.kill(os.getgid(),signal.SIGINT)
        os.kill(light_pid, signal.SIGUSR1)
        with open(pipe_path, "w") as pipe:
            print(2**n_source, source)
            pipe.write(str(2**n_source))
            
        
    



if __name__ == "__main__":
    gen_prio_traffic()