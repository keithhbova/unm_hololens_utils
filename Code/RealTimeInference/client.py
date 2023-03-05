import cv2
import socket
import numpy as np

class UdpVideoCapture:
    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((udp_ip, udp_port))
        self.max_packet_size = 2048
        self.frame_chunks = []

    def read(self):
        while True:
            # Receive a chunk of data
            data, addr = self.sock.recvfrom(self.max_packet_size)

            # Decode the data into a numpy array
            chunk = np.frombuffer(data, dtype=np.uint8)

            # Append the chunk to the list of frame chunks
            self.frame_chunks.append(chunk)

            # If we have received a full frame, decode it and return it
            if len(chunk) < self.max_packet_size:
                # Concatenate the frame chunks into a single numpy array
                frame_data = np.concatenate(self.frame_chunks, axis=None)

                # Decode the frame data into a numpy array
                frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

                # Reset the frame chunks list
                self.frame_chunks = []

                # Return the frame
                return True, frame

    def release(self):
        self.sock.close()


udp_capture = UdpVideoCapture('192.168.42.15', 6969)

while True:
    ret, frame = udp_capture.read()

    if ret:
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

udp_capture.release()
cv2.destroyAllWindows()

