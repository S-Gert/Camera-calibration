from src.calibrate import CameraCalibration
from src.view_raw import open_camera_feed
from src.view_calibrated import open_calibrated_camera_feed
from src.reprojection_accuracy import measure_reprojection_error
import cv2

def main():
    checkerboard_size = (8, 16)

    print("Align camera to center of checkerboard and press Q to calibrate.")
    open_camera_feed()
    calibrator = CameraCalibration(open_window=False, checkerboard_size=checkerboard_size,checkerboard_count=1)
    calibrator.run()
    measure_reprojection_error(checkerboard_size=checkerboard_size, open_window=False)
    print("Q to close window.")
    open_calibrated_camera_feed()

if __name__ == '__main__':
    main()