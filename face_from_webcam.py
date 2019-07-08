import face_recognition
import cv2
import numpy as np
import argparse
import os
import logging
from conf import config

individual_lists = {}
video_capture1 = cv2.VideoCapture(0)
video_capture2 = cv2.VideoCapture(1)
crop_image_dir = config["crop_image_dir"]


def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_image',type=str,help='the directory of known people ')
    parser.add_argument('--crop_image_dir', type=str, )


def CropFace(original_face):
    '''
    FUNCTION: Crop images according webcam
    RETURN: List of crop images
    '''
    crop_imgs = []
    face_locations = face_recognition.face_locations(original_face)
    for i in range(len(face_locations)):
        top = face_locations[i][0]
        right = face_locations[i][1]
        bottom = face_locations[i][2]
        left = face_locations[i][3]

        crop_img = original_face[top:bottom, left:right]
        crop_imgs.append(crop_img)

    return crop_imgs


def FaceProcess(original_frame):
    '''
    Function: GET THE LOCATION AND ENCODINGS OF FRAME
    PARAMS: EACH FRAME OF VIDEO
    RETURN: FACE_LOCATION, FACE_ENCODINGS
    '''

    if type(original_frame) == str:
        image = cv2.imread(original_frame)
        rgb_frame = image[:, :, ::-1]
    else:
        rgb_frame = original_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    return face_locations, face_encodings


def Video(DeviceID):
    '''
    FUNCTION:ENABLE VIDEO ACCORDING FREQUENCY
    '''
    ret, frame = DeviceID.read()
    rgb_frame = frame[:, :, ::-1]  # bgr(opencv) to rgb(this package)
    return frame, rgb_frame


def MatchFace(original_image, new_image):
    '''
    FUNCTION: JUDGE WHEATHER THE FACE DETECED ARE THE SAME FACE
    PARAMS: face_encodings:q
    RETURN:
    '''
    judgement = ''
    threshold = config["threshold"]
    original_image, original_image_encodings = FaceProcess(original_image)
    new_image_locations, new_image_encodings = FaceProcess(new_image)

    # return True OR False of two image_encodings
    matches = face_recognition.compare_faces(original_image_encodings, new_image_encodings[0])
    print(matches)
    # name = "Unknown"

    face_distances = face_recognition.face_distance(original_image_encodings, new_image_encodings[0])
    print(face_distances)
    if face_distances < threshold:
        judgement = 'True'
    else:
        judgement = 'False'
    # best_match_index = np.argmin(face_distances)
    #
    # if matches[best_match_index]:
    #     name = known_face_names[best_match_index]
    return judgement


def Rectangle(locations, face_encodings, frame, name):
    '''
    FUNCTION: DRAW RECTANGLE
    '''
    for (top, right, bottom, left), face_encoding in zip(locations, face_encodings):
        # Draw a box around face
        cv2.rectangle(frame, (left, top), (right,bottom), (0, 0, 255), 2)
        # Draw a label with name
        cv2.rectangle(frame, (left, bottom+35), (right, bottom), (0, 10, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+6, bottom+30), font, 1.0, (255, 255, 255), 1)


def Flags(flags):
    ture_count = 0
    false_count = 0
    for i in range(len(flags)):
        if flags[i] == 'True':
            ture_count += 1
        else:
            false_count += 1
    return ture_count, false_count


if __name__ == "__main__":
    # match = MatchFace('/home/jhx/data/crop/crop48.jpg', '/home/jhx/data/crop/crop432.jpg')
    # print(match)
    fcount = config["frequency_count"]
    icount = config["image_count"]
    frequency = config["frequency"]
    crop_face_dir = config['crop_image_dir']

    while True:
        flags = []
        frame_get, rgb_frame_get = Video(video_capture1)
        locations_get, encodings_get = FaceProcess(frame_get)
        # store_path = crop_face_dir + '/' + str(icount) + '.jpg'
        if fcount % frequency == 0:
            # try:
            crop_imgs = CropFace(frame_get)
            crop_imgs_length = len(crop_imgs)
            face_names = os.listdir(crop_image_dir)
            face_names_num = len(face_names)
            if face_names_num == 0:
                for crop_img in crop_imgs:
                    cv2.imwrite(crop_face_dir + '/' + str(icount) + '.jpg', crop_img)
                    icount += 1

            else:
                for crop_img in crop_imgs:
                    for original_face_name in face_names:
                        old_face = os.path.join(crop_image_dir, original_face_name)
                        flag = MatchFace(old_face, crop_img)
                        flags.append(flag)
                    true, false = Flags(flags)
                    # times = float(match)/float(face_names_num)
                    times_threshold = config["times_threshold"]
                    if false > true:
                        cv2.imwrite(crop_face_dir + '/' + str(icount) + '.jpg', crop_img)
                        icount += 1
                        print("crop and store face image!")
                    else:
                        print('SAME PEOPLE!')
            # except:
            #     print("No FACE!")
        fcount += 1
        Rectangle(locations_get, encodings_get, frame_get, 'people')
        cv2.imshow('Video', frame_get)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_capture1.release()
# video_capture2.release()

cv2.destroyAllWindows()







