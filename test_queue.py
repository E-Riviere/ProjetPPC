import sysv_ipc

key = 128

north = sysv_ipc.MessageQueue(key)
south = sysv_ipc.MessageQueue(key + 1)
west = sysv_ipc.MessageQueue(key + 2)
east = sysv_ipc.MessageQueue(key + 3)

while True:
    i = 0
    try:
        message, t = north.receive(block=False)
        if message:
            print(message.decode())
            i += 1
        message, t = south.receive(block=False)
        if message:
            print(message.decode())
            i += 1
        message, t = west.receive(block=False)
        if message:
            print(message.decode())
            i += 1
        message, t = east.receive(block=False)
        if message:
            print(message.decode())
            i += 1
        
    
    except sysv_ipc.ExistentialError:
        print("No message received")
        break
    except sysv_ipc.BusyError:
        continue
    except Exception as e:
        print(e)
        break
        
    print(i)
    
