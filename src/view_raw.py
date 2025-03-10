import cv2

def open_camera_feed() -> None:
    cap = cv2.VideoCapture(0)
    if (cap.isOpened() == False):
        raise "Error opening video stream."
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            h_center = int(frame.shape[0]/2)
            w_center = int(frame.shape[1]/2)
            rectangle_size = 10
            
            rectangle_start = (w_center+rectangle_size, h_center-rectangle_size)
            rectangle_stop = (w_center-rectangle_size, h_center+rectangle_size)

            cv2.rectangle(frame, rectangle_start, rectangle_stop, (0, 255, 0), 1)
            
            cv2.imshow('Camera feed', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    open_camera_feed()