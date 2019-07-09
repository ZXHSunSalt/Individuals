import cv2
from webcam import cam1, cam2

video_capture1 = cv2.VideoCapture(0)
video_capture2 = cv2.VideoCapture(1)

if __name__ == "__main__":
    cam1 = cam1.Camera1(video_capture1)
    cam1._webcam1()

    cam2 = cam2.Camera2(video_capture2)
    cam2._webcam2()
