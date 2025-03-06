import cv2
import numpy as np

try:
    calib_data = np.load('camera_matrix.npz')
    mtx = calib_data['mtx']
    dist = calib_data['dist']
except:
    raise "camera_matrix.npz Not found"

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    h, w = frame.shape[:2]
    
    # (0 = tight crop, 1 = full view with distortion)
    alpha = 0.6
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), alpha, (w, h))
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    
    x, y, w, h = roi
    if w > 0 and h > 0:
        dst = dst[y:y+h, x:x+w]

    dst = cv2.resize(dst, (frame.shape[1], frame.shape[0]))
    cv2.imshow('Calibrated Video Feed', dst)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
