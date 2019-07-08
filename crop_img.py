import cv2
import face_recognition

zxh_face = face_recognition.load_image_file('/home/jhx/data/zxh.JPG')
rgb_face = zxh_face[:, :, ::-1]
face_locations = face_recognition.face_locations(rgb_face)
print(face_locations)
top = face_locations[0][0]
right = face_locations[0][1]
bottom = face_locations[0][2]
left = face_locations[0][3]
crop_img = rgb_face[top:bottom, left:right]
cv2.imwrite('/home/jhx/data/crop.jpg',crop_img)
