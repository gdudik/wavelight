import socket
import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
GPIO.output(37, GPIO.HIGH)

# TCP server configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 9999

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        if "RUNNING" in data:
            GPIO.output(37, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(37, GPIO.HIGH)

    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        GPIO.cleanup()
