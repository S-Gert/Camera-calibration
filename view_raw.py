import cv2

def main() -> None:
    cap = cv2.VideoCapture(0)
    if (cap.isOpened() == False):
        raise "Error opening video stream."
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Camera feed', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()