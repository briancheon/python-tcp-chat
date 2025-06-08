import socket
import threading
import pygame
import sys
import time

def get_username():
    pygame.init()
    WIDTH, HEIGHT = 600, 50
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Enter Username")

    FONT = pygame.font.Font(None, 36)
    input_box = pygame.Rect(150, 7, 440, 36)
    input_text = ""
    color = pygame.Color('gray15')

    done = False

    while not done:
        screen.fill((255, 255, 255))
        enter_username = FONT.render("Username: ", True, (0, 0, 0))
        txt_surface = FONT.render(input_text, True, (0, 0, 0))

        screen.blit(enter_username, (5, 12))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip() != "":
                        done = True
                        break
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    pygame.quit()
    return input_text.strip()

# === Username ===
username = get_username()

# === Socket Setup ===
SERVER = '127.0.0.1'
PORT = 12345
ADDRESS = (SERVER, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)
client_socket.send(username.encode('utf-8'))  # Send username to server for recognition

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 600, 425
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Pygame Chat Client: {username}")

FONT = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
input_text = ""
messages = []

# === Colors ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)

def draw_window():
    screen.fill(WHITE)
    y_offset = 10

    recent_messages = messages[-5:]

    for sender, msg in recent_messages:
        is_self = (sender == username)
        text_color = BLACK
        bubble_color = (200, 230, 255) if is_self else (220, 220, 220)

        name_surface = FONT.render(sender, True, (100, 100, 100))
        msg_surface = FONT.render(msg, True, text_color)
        padding = 10
        bubble_width = msg_surface.get_width() + 2 * padding
        bubble_height = msg_surface.get_height() + 2 * padding

        x_pos = WIDTH - bubble_width - padding if is_self else padding
        name_x_pos = WIDTH - name_surface.get_width() - padding if is_self else padding

        screen.blit(name_surface, (name_x_pos, y_offset))
        y_offset += name_surface.get_height() + 2

        pygame.draw.rect(screen, bubble_color,
                         (x_pos, y_offset, bubble_width, bubble_height), border_radius=8)

        screen.blit(msg_surface, (x_pos + padding, y_offset + padding))

        y_offset += bubble_height + 10

    pygame.draw.rect(screen, LIGHT_GRAY, input_box)
    txt_surface = FONT.render(input_text, True, BLACK)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

    pygame.display.update()

def receive_messages():
    print("[DEBUG] Receiver thread started")
    while True:
        try:
            raw_msg = client_socket.recv(1024).decode('utf-8')
            if not raw_msg:
                print("[INFO] Server closed the connection.")
                break

            print(f"[INFO] Received Message: {raw_msg}")
            if ": " in raw_msg:
                sender, content = raw_msg.split(": ", 1)
                messages.append((sender, content))

            draw_window()  # Ensure the window is updated with new messages

        except Exception as e:
            print(f"[ERROR] {e}")
            break

receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# === Main Loop ===
run = True
while run:
    clock.tick(30)
    draw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client_socket.send("__exit__".encode('utf-8'))
            time.sleep(0.1)
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_text.strip() != "":
                    try:
                        usr_msg = f"{username}: {input_text.strip()}"
                        client_socket.send(usr_msg.encode('utf-8'))
                        messages.append((username, input_text.strip()))
                        input_text = ""
                    except Exception as e:
                        print(f"[ERROR] Failed to send message: {e}")

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

pygame.quit()
sys.exit()