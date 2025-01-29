import sysv_ipc
import time
import random
first_key = 128
 
north = sysv_ipc.MessageQueue(first_key, sysv_ipc.IPC_CREAT)
south = sysv_ipc.MessageQueue(first_key + 1, sysv_ipc.IPC_CREAT)
west = sysv_ipc.MessageQueue(first_key + 2, sysv_ipc.IPC_CREAT)
east = sysv_ipc.MessageQueue(first_key + 3, sysv_ipc.IPC_CREAT)

def gen_traffic():
    voiture = ""
    i = 0
    while i < 10:
        try:
            direction = ["North", "South", "West", "East"]
            source = random.choice(direction)
            destination = random.choice(direction)
            voiture = f"Car{i}"
            message = f"{destination},{voiture}"
            print(source+ ',' + message)
            message = message.encode()
            if source == "North":
                north.send(message)
            elif source == "South":
                south.send(message)
            elif source == "West":
                west.send(message)
            else:
                east.send(message)

            i += 1
        
        except Exception as e:
            print(e)
    print(i)
    time.sleep(10)
    north.remove()
    south.remove()
    west.remove()
    east.remove()



if __name__ == "__main__":
    gen_traffic()