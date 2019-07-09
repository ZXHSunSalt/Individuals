from webcam.__init__ import *
import func

class Camera2():
    def __init__(self, video_capture):
        self.video_caputre = video_capture

        self.fcount = config['frequency_count']
        self.frequency = config['frequency']
        self.crop_face_dir = config['crop_image_dir']
        self.db = db.Database('face_recognition')

    def _webcam2(self):
        while True:
            frame_get, rgb_frame_get = func.video(self.video_caputre)
            locations_get, encodings_get = func.face_process(frame_get)

            if self.fcount % self.frequency == 0:
                try:
                    # data_transformed_from_db, crop_imgs, crop_imgs_length, data_transformed_length = func.get_transform_data(frame_get)

                    # get crop_image and the encoding of image
                    crop_imgs = func.crop_face(frame_get)  # crom_imgs-> nparray
                    crop_imgs_length = len(crop_imgs)

                    # get all encodings form database and transfome them from array_str to list
                    all_data_from_db = self.db._get_data('face_encodings')
                    data_transformed_from_db = func.array_str2list(all_data_from_db)
                    data_transformed_length = len(data_transformed_from_db)

                    if data_transformed_length == 0:
                        print('no record in database!')
                    else:
                        for i in range(crop_imgs_length):
                            crop_img_encoding = face_recognition.face_encodings(crop_imgs[i]) #crop_img_encoding -> list
                            for j in range(data_transformed_length):
                                flag_list = []
                                faceid = data_transformed_from_db[j][0]
                                encoding = data_transformed_from_db[j] #encoding -> list
                                flag_list.append(encoding[1])
                                t_count, f_count = func.match_face(flag_list, crop_img_encoding[0])
                                if t_count == 1:
                                    condition = "faceid=" + faceid
                                    self.db._delete_data('face_encodings', condition)
                                    self.db._commit()
                                    print('delete one record!')
                                else:
                                    print("people exists!")

                except:
                    print('No face or Occur error')


            func.rectangle(locations_get, encodings_get, frame_get, 'people')
            cv2.imshow('Video', frame_get)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


