import cv2
import numpy as np


img_captures = 1
CHECKERBOARD = (8, 6) # Checkerboard dimensions

objpoints = []  # 3D points in real-world space
imgpoints = []  # 2D points in image plane

# Prepare object points (0,0,0), (1,0,0), (2,0,0), ..., (8,5,0)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

cap = cv2.VideoCapture(0)

print("'c' to capture a frame for calibration, 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    
    if found:
        cv2.drawChessboardCorners(frame, CHECKERBOARD, corners, found)
    
    cv2.imshow('Camera Feed', frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('c') and found:
        objpoints.append(objp)
        imgpoints.append(corners)
        print(f"Frame {img_captures} captured")
        img_captures += 1
    
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if objpoints and imgpoints:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez('camera_matrix.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    
    print(f"Camera matrix: \n{mtx}\nDistortion coefficients: {dist}")
else:
    print("Not enough valid frames captured for calibration.")
