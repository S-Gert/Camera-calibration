import cv2
import numpy as np

'''
Reprojection error measures how well the camera calibration model fits the detected checkerboard points.
an error of 0.1 or below is excellent but above 1.0 is pretty terrible.
'''

def load_calibration(file_path='src/camera_matrix.npz'):
    try:
        with np.load(file_path) as data:
            mtx = data['mtx']
            dist = data['dist']
            return mtx, dist
    except FileNotFoundError:
        print("Camera matrix not found.")
        return None, None

def measure_reprojection_error(checkerboard_size=(8, 16), open_window=True):
    mtx, dist = load_calibration()
    if mtx is None or dist is None:
        return
    
    error_array = []
    total_errors_to_average = 50

    objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)
    
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)
        
        if found:
            _, rvecs, tvecs = cv2.solvePnP(objp, corners, mtx, dist)
            projected_points, _ = cv2.projectPoints(objp, rvecs, tvecs, mtx, dist)
            
            error = cv2.norm(corners, projected_points, cv2.NORM_L2) / len(projected_points)
            if len(error_array) < total_errors_to_average:
                error_array.append(error)
            
            for corner, proj in zip(corners, projected_points):
                cv2.circle(frame, tuple(corner.ravel().astype(int)), 5, (0, 255, 0), -1)
                cv2.circle(frame, tuple(proj.ravel().astype(int)), 5, (0, 0, 255), -1)
        
        if open_window:
            cv2.imshow('Reprojection error', frame)
            if found:
                print(f"Reprojection error: {error:.4f}")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        elif len(error_array) >= total_errors_to_average:
            break
    
    print(f"Average reprojection error: {(sum(error_array[:total_errors_to_average])/total_errors_to_average):.4f}")
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    measure_reprojection_error(checkerboard_size=(8, 16))