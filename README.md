# Python TCP Chat Application

A simple multi-client TCP chat application implemented in Python.  
This project includes:  
- A **chat server** (`chat_server.py`) that handles multiple clients and message broadcasting.  
- A **command-line chat client** (`chat_client.py`) to connect and chat with the server.  
- A **GUI chat client** (`chat_client_gui.py`) built with Pygame for a more interactive chat experience.

---

## Features

- Multi-threaded server supporting multiple clients simultaneously.
- Username-based messaging and user join/leave notifications.
- Graceful disconnects and server shutdown.
- GUI client with message bubbles and real-time updates using Pygame.
- Command-line client for quick and easy chatting.

---

## Requirements

- Pygame (only for the GUI client)

Install pygame with:  
```bash
pip install pygame
```  

## Usage
### 1. Start the Server
```bash
python chat_server.py
```
The server runs on localhost (127.0.0.1) and port 12345 by default.
Type exit in the server console to shut down the server.

2. Run the Command-Line Client
```bash
python chat_client.py
```
Connects to the server on 127.0.0.1:12345.

Enter messages to send.

Type exit to disconnect.

3. Run the Pygame GUI Client
```bash
python chat_client_gui.py
```
Enter your username on start.

Use the GUI window to send and receive messages.

Close the window or type exit to leave the chat.

## How it Works
The server accepts connections, handles each client in a separate thread, and broadcasts messages to all other connected clients.

Clients send their username on connection for identification.

Messages are sent as UTF-8 encoded strings with a format like username: message.

The GUI client displays messages with styled bubbles differentiating your messages from others.

## File Overview
chat_server.py - TCP server code with client management and broadcast.

chat_client.py - Simple terminal-based client for chat.

chat_client_gui.py - Pygame-based graphical client interface.

License
This project is released under the MIT License.

Contact
For questions or contributions, feel free to open an issue or a pull request.

