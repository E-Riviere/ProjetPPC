import socket






HOST = "localhost"
PORT = 8080


if __name__ == "__main__":
    try:
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


                    
            