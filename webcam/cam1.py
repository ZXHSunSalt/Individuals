# import conf
from webcam.__init__ import *
from database import db
import func
import time

class Camera1(object):
    def __init__(self, video_capture):
        self.video_capture = video_capture

        self.fcount = config["frequency_count"]
        self.icount = config["image_count"]
        self.frequency = config["frequency"]
        self.crop_face_dir = config['crop_image_dir']
        self.db = db.Database('face_recognition')

    def _webcam1(self):
        while True:
            flags = []

            frame_get, rgb_frame_get = func.video(self.video_capture)
            locations_get, encodings_get = func.face_process(frame_get)

            if self.fcount % self.frequency == 0:
                try:
                    #using time stamp as faceid
                    current_time = time.time()

                    # get crop_image and the encoding of image
                    crop_imgs = func.crop_face(frame_get)  # crom_imgs-> nparray
                    crop_imgs_length = len(crop_imgs)

                    # get all encodings form database and transfome them from array_str to list
                    all_data_from_db = self.db._get_data('face_encodings')
                    data_transformed_from_db = func.array_str2list(all_data_from_db)
                    data_transformed_length = len(data_transformed_from_db)

                    if data_transformed_length == 0:
                        for i in range(crop_imgs_length):
                            crop_img_encoding = face_recognition.face_encodings(crop_imgs[i])
                            self.db._insert_data('face_encodings', ['faceid', 'encoding'], [str(current_time), str(crop_img_encoding[0].tolist())])
                            self.db._commit()
                            print('insert one record!')
                    else:
                        for i in range(crop_imgs_length):
                            crop_img_encoding = face_recognition.face_encodings(crop_imgs[i])

                            t_count, f_count = func.match_face(data_transformed_from_db, crop_img_encoding)
                            if t_count == 0:
                                self.db._insert_data('face_encodings', ['faceid', 'encoding'], [str(current_time), str(crop_img_encoding[0].tolist())])
                                self.db._commit()
                                print('insert one record!')
                            else:
                                print("people exists!")
                except:
                    print('NO Face OR Occur Error')

            func.rectangle(locations_get, encodings_get, frame_get, 'people')
            cv2.imshow('Video', frame_get)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break