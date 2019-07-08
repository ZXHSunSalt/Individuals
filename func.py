import cv2
import argparse
import face_recognition
import numpy as np

from database import db
from conf import config


def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_image', type=str, help='the directory of known people ')
    parser.add_argument('--crop_image_dir', type=str, )

def crop_face(original_face):
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

def face_process(original_frame):
    '''
    Function: GET THE LOCATION AND ENCODINGS OF FRAME(store image to local)
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

def video(DeviceID):
    '''
    FUNCTION:ENABLE VIDEO ACCORDING FREQUENCY
    '''
    ret, frame = DeviceID.read()
    rgb_frame = frame[:, :, ::-1]  # bgr(opencv) to rgb(this package)
    return frame, rgb_frame

def match_face(encodings_from_db, new_crop_encoding):
    '''
    FUNCTION: JUDGE WHEATHER THE FACE DETECED ARE THE SAME FACE
    PARAMS: 1 processed image encoding from database
            2 crop image encoding from each frame of video
    RETURN: True OR False
    '''
    t_count = 0
    f_count = 0
    threshold = config["threshold"]

    matches = face_recognition.compare_faces(encodings_from_db, new_crop_encoding[0])

    # the first params of face_distance : -> list of array, the second para -> nparray
    distances = face_recognition.face_distance(encodings_from_db, new_crop_encoding[0])
    max_distance = np.argmax(distances)

    for item in matches:
        if item == True:
            t_count += 1
        else:
            f_count += 1
    return t_count, f_count

def rectangle(locations, face_encodings, frame, name):
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

def _flags(flags):
    ture_count = 0
    false_count = 0
    for i in range(len(flags)):
        if flags[i] == 'True':
            ture_count += 1
        else:
            false_count += 1
    return ture_count, false_count

def array_str2list(data_from_database):

    peoples = {}
    new_lists = []
    for row in data_from_database:
        faceid = row[0]
        encoding = row[1]
        peoples[faceid] = encoding

        item = np.array(eval(peoples[faceid]))
        new_lists.append(item)
    return new_lists

def get_transform_data(frame):
    # get crop_image and the encoding of image
    crop_imgs = crop_face(frame)  # crom_imgs-> nparray
    crop_imgs_length = len(crop_imgs)

    # get all encodings form database and transfome them from array_str to list
    all_data_from_db = db._get_data('face_encodings')
    data_transformed_from_db = array_str2list(all_data_from_db)
    data_transformed_length = len(data_transformed_from_db)

    return data_transformed_from_db, crop_imgs, crop_imgs_length, data_transformed_length