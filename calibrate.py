import cv2
import numpy as np
import time

class CameraCalibration:
    def __init__(self, checkerboard_size=(8, 6)):
        self.checkerboard_size = checkerboard_size
        self.objpoints = []  # 3D real world points
        self.imgpoints = []  # 2D image points
        self.captured_masks = []  # masks for detected checkerboards
        self.img_captures = 1
        self.objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2) # object point plain

        self.cap = cv2.VideoCapture(0)

        self.camera_feed_window_warning = False

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return None, None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # apply masks to already captured checkerboards
        for mask in self.captured_masks:
            cv2.fillPoly(gray, [mask], (0, 0, 0))

        return frame, gray

    def process_frame(self, frame, gray):
        found, corners = cv2.findChessboardCorners(gray, self.checkerboard_size, None)

        if found:
            cv2.drawChessboardCorners(frame, self.checkerboard_size, corners, found)

        try:
            cv2.imshow('Camera Feed', frame)
            cv2.waitKey(1)
        except:
            if self.camera_feed_window_warning == False:
                print("Unable to open camera feed window.")
                self.camera_feed_window_warning = True
            else:
                pass

        if found:
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners)
            print(f"Checkerboard {self.img_captures}/5 captured")
            self.img_captures += 1

            # mask for captured checkerboard
            hull = cv2.convexHull(corners)
            self.captured_masks.append(hull.astype(int))

    def save_calibration(self, gray_shape):
        if self.objpoints and self.imgpoints:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
                self.objpoints, self.imgpoints, gray_shape[::-1], None, None
            )
            np.savez('camera_matrix.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

            print(f"Camera matrix:\n{mtx}\nDistortion coefficients:\n{dist}")

    def run(self):
        old_time = 0
        while True:
            new_time = time.time()
            frame, gray = self.capture_frame()
            if frame is None or gray is None:
                break
            
            if new_time > old_time + 0.1:
                self.process_frame(frame, gray)
                old_time = time.time()

            if self.img_captures > 5:
                break

        self.cap.release()
        cv2.destroyAllWindows()

        if self.imgpoints:
            self.save_calibration(gray.shape)

if __name__ == '__main__':
    calibrator = CameraCalibration()
    calibrator.run()