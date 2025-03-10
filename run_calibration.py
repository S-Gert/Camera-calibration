from src.calibrate import CameraCalibration
from src.view_raw import open_camera_feed
from src.view_calibrated import open_calibrated_camera_feed
import cv2

def main():
    open_camera_feed()
    calibrator = CameraCalibration(open_window=False)
    calibrator.run()
    # TODO: evaluate calibration accuracy 
    open_calibrated_camera_feed()

if __name__ == '__main__':
    main()