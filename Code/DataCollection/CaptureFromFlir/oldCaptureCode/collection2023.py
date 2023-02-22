import numpy as np
import cv2
# Camera number can be either 0 or 1

USING_SSH = False

print(f"Trying to open camera at index 0")
camera_number = 1
cap = cv2.VideoCapture(camera_number)

 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoName = input("Input the name of the video here: ") + ".avi"
out = cv2.VideoWriter(videoName, fourcc, 20.0, (640, 480))
print(f"press q on the window to save")
 
# loop runs if capturing has been initialized. 
while(True):
     ret, frame = cap.read()
     out.write(frame)
     if(USING_SSH):
        cv2.imshow('Original', frame)
     # Wait for 'a' key to stop the program 
     if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
out.release()
cv2.destroyAllWindows()

