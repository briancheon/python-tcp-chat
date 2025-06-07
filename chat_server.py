import socket
import threading

# Set Server
SERVER = '127.0.0.1'  # localhost
PORT = 12345

ADDRESS = (SERVER, PORT)

# Server Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET : Uses IPv4 Addressing, SOCK_STREAM : Receive TCP

# Assign IP Address and PORT to socket
server_socket.bind(ADDRESS)

# Enable server to accept connections
server_socket.listen()
print(f"[STARTED] Server listening on {SERVER}:{PORT}")

# Dictionary for client connection management
clients = {}

def broadcast(message, sender_socket=None):
    """
    Sends a message to all clients except the sender.
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"[ERROR] Failed to send message to {clients[client]}: {e}")

def handle_client(client_socket, client_address):
    """
    Handle communication with a single client
    """
    print(f"[NEW CONNECTION] {client_address} connected.")
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(clients.values())
        broadcast(f"[{username}] has joined the chat.".encode('utf-8'), sender_socket=client_socket)

        while True:
            message = client_socket.recv(1024)
            print(message)
            if not message:
                break
            decoded = message.decode('utf-8')

            if decoded == "__exit__":
                break

            message_content = decoded.split(": ", 1)[1] if ": " in decoded else decoded
            print(f"[INFO] Message Received: {message_content}")
            formatted_msg = f"{username}: {message_content}"
            print(f"[INFO] Sending formatted message: {formatted_msg}")
            broadcast(formatted_msg.encode('utf-8'), sender_socket=client_socket)

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        print("Here")
        disconnect_client(client_socket, client_address)

def disconnect_client(client_socket, client_address):
    """
    Disconnect a client
    """
    if client_socket in clients:
        username = clients[client_socket]
        print(f"[DISCONNECTED] {username} ({client_address}) disconnected.")
        broadcast(f"[{username}] has left the chat.".encode('utf-8'), sender_socket=client_socket)
        del clients[client_socket]
    try:
        client_socket.close()
    except Exception as e:
        print(f"[ERROR] during socket close: {e}")
        
def monitor_for_exit():
    """
    Monitors CLI for 'exit' input to shut down the server.
    """
    while True:
        command = input()
        if command.strip().lower() == "exit":
            print("[SHUTDOWN] Exit command received. Closing server socket...")
            server_socket.close()
            break

def start_server():
    """
    Main Server Loop to accept new connections
    """
    # Start the exit-monitoring thread
    threading.Thread(target=monitor_for_exit, daemon=True).start()

    try:
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
                thread.start()
            except OSError:
                # Raised when server_socket is closed
                break
    finally:
        print("[SHUTDOWN] Server shutting down.")

if __name__ == "__main__":
    start_server()