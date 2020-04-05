import socket 
import threading

# Define header, port and grab local IP address

HEADER = 64 # bytes
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Make a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind server to address
server.bind(ADDR)

def handle_client(conn, addr):
    # This function runs concurrently for each client
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    
    while connected:
        # Wait to recieve information from the client
        # recv() takes how many bytes are actually recieved from the client
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        # Make sure that the message has some content or we get an error
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                    
            print(f"[{addr}] {msg}")
            conn.send( "Message received".encode(FORMAT) )
            
    # Handle client disconnecting
    conn.close()

def start():
    server.listen()
    print(f"[LISTTENING] Server is listening on {SERVER}")
    while True:
        # This line blocks and waits for a new connection
        conn, addr = server.accept()
        
        # Start a new thread using handle_client
        # When a new connection occurs, pass that information to handle_client
        thread = threading.Thread( target = handle_client, args=(conn, addr) )
        thread.start()
        
        # The "start" thread is always running, so -1 to determine the actual external connections
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")

start()
