import cv2

def open_camera_feed(middle_rectangle_size = 0, show_checkerboard = False, checkerboard_size = (0, 0)) -> None:
    cap = cv2.VideoCapture(0)
    if (cap.isOpened() == False):
        raise "Error opening video stream."
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if middle_rectangle_size != 0:
                h_center = int(frame.shape[0]/2)
                w_center = int(frame.shape[1]/2)
                
                rectangle_start = (w_center+middle_rectangle_size, h_center-middle_rectangle_size)
                rectangle_stop = (w_center-middle_rectangle_size, h_center+middle_rectangle_size)
                cv2.rectangle(frame, rectangle_start, rectangle_stop, (0, 255, 0), 1)
            if show_checkerboard:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                found, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)
                if found:
                    cv2.drawChessboardCorners(frame, checkerboard_size, corners, found)

            cv2.imshow('Camera feed', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    checkerboard_size = (12, 20)
    open_camera_feed(show_checkerboard=True, checkerboard_size=checkerboard_size)