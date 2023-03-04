import cv2
import socket
import numpy as np

# Define the IP address and port of the UDP sender
UDP_IP:str = ''
UDP_PORT:int = 6969

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port
sock.bind((UDP_IP, UDP_PORT))

# Define the maximum packet size
MAX_PACKET_SIZE = 1024

# Initialize the frame variable
frame_chunks = []

while True:
    # Receive a chunk of data
    data, addr = sock.recvfrom(MAX_PACKET_SIZE)

    # Decode the data into a numpy array
    chunk = np.frombuffer(data, dtype=np.uint8)

    # Append the chunk to the list of frame chunks
    frame_chunks.append(chunk)

    # If we have received a full frame, decode it and display it
    if len(chunk) < MAX_PACKET_SIZE:
        # Concatenate the frame chunks into a single numpy array
        frame_data = np.concatenate(frame_chunks, axis=None)

        # Decode the frame data into a numpy array
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

        # Display the frame
        cv2.imshow('frame', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Reset the frame chunks list
        frame_chunks = []

# Release everything
cv2.destroyAllWindows()
