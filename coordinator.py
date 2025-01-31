import socket






HOST = "localhost"
PORT = 8080


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                conn, addr = server_socket.accept()
                with conn:
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
                        except:
                            print("Error")
                            break
                        
                    
            