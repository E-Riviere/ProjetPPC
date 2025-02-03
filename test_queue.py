import sysv_ipc

key = 128

north = sysv_ipc.MessageQueue(key)
south = sysv_ipc.MessageQueue(key + 1)
west = sysv_ipc.MessageQueue(key + 2)
east = sysv_ipc.MessageQueue(key + 3)
i = 0
while True:
    
    try:
        try: 
            message, t = north.receive(block=False)

            print("N",message.decode())
            i += 1
            print(i)
        except sysv_ipc.BusyError:
            pass
        

        try:
            message, t = south.receive(block=False)
            print("S",message.decode())
            i += 1
            print(i)
        except sysv_ipc.BusyError:
            pass

        try:
            message, t = west.receive(block=False)
            print("W",message.decode())
            i += 1
            print(i)
        except sysv_ipc.BusyError:
            pass

        try:
            message, t = east.receive(block=False)
            print("E",message.decode())
            i += 1
            print(i)
        except sysv_ipc.BusyError:
            pass
        
    
    except sysv_ipc.ExistentialError:
        print("No message received")
        break
    except Exception as e:
        print(e)
        break
        
    #print(i)
    if i >= 2000:
        break

print(i)
north.remove()
south.remove()
west.remove()
east.remove()
