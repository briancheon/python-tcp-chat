import socket
import threading

SERVER = "127.0.0.1"
PORT = 12345

ADDRESS = (SERVER, PORT)

# Client Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_messages():
    """
    Thread function to receive message from the server
    """
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                # Server closed connection
                print(f"[INFO] Disconnected from server.")
                break
        
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            break

def send_messages():
    """
    Loop to read input from user and send to the server
    """
    while True:
        message = input()
        if message.lower() == 'exit':
            print(f"[INFO] Exiting chat.")
            client_socket.close()
            break

        try:
            client_socket.send(message.encode('utf-8'))

        except Exception as e:
            print(f"[ERROR] Could not send message: {e}")
            break

if __name__ == "__main__":
    try:
        client_socket.connect(ADDRESS)
        print(f"[INFO] Connected to chat server at {SERVER}:{PORT}")

    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        exit(1)
    
    # Start thread to listen for incoming messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    # Main thread handles sending messages
    send_messages()