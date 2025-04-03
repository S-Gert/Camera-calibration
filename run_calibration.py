import tkinter as tk
from tkinter import messagebox
from src.calibrate import CameraCalibration
from src.view_raw import open_camera_feed
from src.view_calibrated import open_calibrated_camera_feed
from src.reprojection_accuracy import measure_reprojection_error
import cv2

checkerboard_corner_height_count = 12
checkerboard_corner_width_count = 20
checkerboard_count = 1

def run_calibration():
    try:
        checkerboard_corner_height_count = int(height_entry.get())
        checkerboard_corner_width_count = int(width_entry.get())
        checkerboard_count = int(count_entry.get())
        checkerboard_size = (checkerboard_corner_height_count, checkerboard_corner_width_count)

        root.destroy()
        print("Align camera to center of checkerboard and press Q to calibrate.")
        open_camera_feed(show_checkerboard=True, checkerboard_size=checkerboard_size)
        calibrator = CameraCalibration(open_window=False, checkerboard_size=checkerboard_size, checkerboard_count=checkerboard_count)
        calibrator.run()
        measure_reprojection_error(checkerboard_size=checkerboard_size, open_window=True)
        print("Q to close window.")
        open_calibrated_camera_feed()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integer values for all fields.")

root = tk.Tk()
root.title("Camera Calibration")

tk.Label(root, text="Checkerboard Height:").grid(row=0, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=0, column=1)
height_entry.insert(0, f"{checkerboard_corner_height_count}")

tk.Label(root, text="Checkerboard Width:").grid(row=1, column=0)
width_entry = tk.Entry(root)
width_entry.grid(row=1, column=1)
width_entry.insert(0, f"{checkerboard_corner_width_count}")

tk.Label(root, text="Checkerboard Count:").grid(row=2, column=0)
count_entry = tk.Entry(root)
count_entry.grid(row=2, column=1)
count_entry.insert(0, f"{checkerboard_count}")

run_button = tk.Button(root, text="Run Calibration", command=run_calibration)
run_button.grid(row=3, column=0, columnspan=2)

if __name__ == '__main__':
    root.mainloop()
