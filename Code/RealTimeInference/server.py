import cv2
import socket

# Define the capture device
cap = cv2.VideoCapture(0)

# Define the IP address and port of the UDP receiver
UDP_IP:str = '10.88.148.150'
UDP_PORT:int = 6969

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the maximum packet size
MAX_PACKET_SIZE = 1024

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Encode the frame as a string of bytes
        data = cv2.imencode('.jpg', frame)[1].tobytes()

        # Split the data into smaller chunks
        chunks = [data[i:i+MAX_PACKET_SIZE] for i in range(0, len(data), MAX_PACKET_SIZE)]

        # Send each chunk to the UDP receiver
        for chunk in chunks:
            sock.sendto(chunk, (UDP_IP, UDP_PORT))

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release everything
cap.release()
cv2.destroyAllWindows()
