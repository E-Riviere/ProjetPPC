import sysv_ipc
import time
import random
first_key = 128
 
north = sysv_ipc.MessageQueue(first_key, sysv_ipc.IPC_CREAT)
south = sysv_ipc.MessageQueue(first_key + 1, sysv_ipc.IPC_CREAT)
west = sysv_ipc.MessageQueue(first_key + 2, sysv_ipc.IPC_CREAT)
east = sysv_ipc.MessageQueue(first_key + 3, sysv_ipc.IPC_CREAT)

def gen_prio_traffic():
    voiture = ""
    i = 0
    while i < 1000:
        try:
            direction = ["North", "South", "West", "East"]
            source = random.choice(direction)
            destination = random.choice(direction)
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
        
        except Exception as e:
            print(e)
    print(i)
    



if __name__ == "__main__":
    gen_prio_traffic()