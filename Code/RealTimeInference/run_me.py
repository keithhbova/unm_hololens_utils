from flask import Flask, render_template, send_from_directory, Response
import cv2
import base64

app = Flask(__name__)

import socket
import numpy as np

username = 'admin'
password = ""
endpoint = ''
ip = '192.168.42.18:554'



class UdpVideoCapture:
    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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



# Initialize the two cameras
cap1 = UdpVideoCapture('0.0.0.0', 6969)
cap2 = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip}/{endpoint}')

# Route for camera 1
@app.route("/cam1")
def cam1():
    ret, frame = cap1.read()
    _, jpeg = cv2.imencode('.jpg', frame)
    frame = base64.b64encode(jpeg.tobytes()).decode("utf-8")
    return frame

# Route for camera 2
@app.route("/cam2")
def cam2():
    ret, frame = cap2.read()
    _, jpeg = cv2.imencode('.jpg', frame)
    frame = base64.b64encode(jpeg.tobytes()).decode("utf-8")
    return frame

@app.route("/frame/<int:camera_num>")
def frame(camera_num):
    if camera_num == 1:
        cap = cap1
    elif camera_num == 2:
        cap = cap2
    else:
        return "Invalid camera number"

    ret, frame = cap.read()
    _, jpeg = cv2.imencode('.jpg', frame)
    frame = base64.b64encode(jpeg.tobytes()).decode("utf-8")
    return frame

@app.route("/")
def home():
    # Get the width and height of camera 1's frames
    ret, frame = cap1.read()
    height1, width1, _ = frame.shape

    # Get the width and height of camera 2's frames
    ret, frame = cap2.read()
    height2, width2, _ = frame.shape

    # Return the template with both camera's dimensions
    return render_template("index.html", width1=width1, height1=height1, width2=width2, height2=height2)

@app.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory('assets', path)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port="5000", threaded=True)
