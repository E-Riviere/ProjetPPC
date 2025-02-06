import sysv_ipc
import time
import random
first_key = 128
 
north = sysv_ipc.MessageQueue(first_key, sysv_ipc.IPC_CREAT)
south = sysv_ipc.MessageQueue(first_key + 1, sysv_ipc.IPC_CREAT)
west = sysv_ipc.MessageQueue(first_key + 2, sysv_ipc.IPC_CREAT)
east = sysv_ipc.MessageQueue(first_key + 3, sysv_ipc.IPC_CREAT)

def gen_traffic():
    while True:
        try:
            nb_veh = int(input("Entrer le nombre de véhicule normal à générer (-1 to test priority) : "))
            break
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
    voiture = ""
    i = 0
    
    if nb_veh == -1:
        north.send("East,BlockedCar1".encode())
        north.send("East,BlockedCar2".encode())
        for j in range(10):
            south.send(f"North,BlockingCar{j}".encode())
    while i < nb_veh:
        try:
            direction = ["South", "East", "West", "North"]
            source = direction[random.randint(0, 3)]
            direction.remove(source)
            destination = direction[random.randint(0, 2)]
            voiture = f"Car{i}"
            message = f"{destination},{voiture}"
            print(source+ ',' + message)
            message = message.encode()
            if source == "North":
                north.send(message, type=1)
            elif source == "South":
                south.send(message, type=1)
            elif source == "West":
                west.send(message, type=1)
            else:
                east.send(message, type=1)

            i += 1
            time.sleep(random.random()/10)
        except Exception as e:
            print(e)
    
    north.send("".encode(),type=3)
    print(i)
    



if __name__ == "__main__":
    gen_traffic()