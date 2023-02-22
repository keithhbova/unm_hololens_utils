from flask import Flask, render_template, send_from_directory
import cv2
import base64

app = Flask(__name__)

# Initialize the two cameras
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture("https://FireFighterPortal:firefighter@192.168.30.3/api/holographic/stream/live_high.mp4?holo=true&pv=true&mic=true&loopback=true")

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
        cap = cv2.VideoCapture(0)
    elif camera_num == 2:
        cap = cv2.VideoCapture(0)
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
    return render_template("project-page.html", width1=width1, height1=height1, width2=width2, height2=height2)

@app.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory('assets', path)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
