import socket
import signal
import os
import time
def sig_usr1_handler(pid):
    time.sleep(2)
    os.kill(pid, signal.SIGUSR2)

import shared_memory_process
HOST = "localhost"
PORT = 8080


if __name__ == "__main__":
    try:
        
        data_process=shared_memory_process.shared_memory_manager('coordinator')
        light_pid=int([i for i in data_process if i[0]=='light'][0][1])
        signal.signal(signal.SIGUSR1, lambda a, b: sig_usr1_handler(light_pid))
        conn = None
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        while True:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn, addr = server_socket.accept()
            print("Connected by", addr)
            for i in range(10):
                if i % 2 == 0:
                    data = [["R","R","G","G"],[],["Car1","Car2"],["Car3"],[],"An action"]
                else:
                    data = [["G","G","R","R"],["Car1","Car2"],["Car3"],[],[],"No action"]
                data = str(data)
                print(f"Sending data: {data}")
                data = data.encode()
                try:
                    conn.send(data)
                    conn.recv(1024)
                except Exception as e:
                    print("Error", e)
                    break


    except KeyboardInterrupt as e:
        server_socket.close()
        client_socket.close()
        if conn != None:
            conn.close()
        print("\nServer closed")
        print("KeyboardInterrupt")
        exit()
    except Exception as e:
        print(e)
        server_socket.close()
        client_socket.close()
        if conn != None:
            conn.close()
        print("Server closed")
        exit()


                    
            