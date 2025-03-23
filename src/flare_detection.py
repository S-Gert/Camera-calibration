import cv2
import numpy as np

# Open the webcam (0 for default camera, change if using external camera)
cap = cv2.VideoCapture(0)

# Set resolution (optional, depends on your camera)
#cap.set(3, 640)  # Width
#cap.set(4, 480)  # Height

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    lower_thresh = 240
    upper_thresh = 255
    _, thresh = cv2.threshold(blurred, lower_thresh, upper_thresh, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    flare_detected = frame.copy()
    cv2.drawContours(flare_detected, contours, -1, (0, 0, 255), 2)  # Red outlines

    combined_frame = np.hstack((frame, flare_detected))
    cv2.imshow("Camera Feed (Left) | Flare Detection (Right)", combined_frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
