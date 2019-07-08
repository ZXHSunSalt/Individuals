import cv2
from webcam import cam1

video_capture1 = cv2.VideoCapture(2)

if __name__ == "__main__":
    cam1 = cam1.Camera1(video_capture1)
    cam1._webcam1()
