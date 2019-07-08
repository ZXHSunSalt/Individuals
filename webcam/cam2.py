from webcam.__init__ import *
import func

class Camera2():
    def __init__(self, video_capture):
        self.video_caputre = video_capture
        self.fcount = config['frequency_count']
        self.frequency = config['frequency']
        self.crop_face_dir = config['crop_image_dir']
        self.db = db.Database('face_recognition')

    def cam2(self):
        while True:
            frame_get, rgb_frame_get = func.video(self.video_capture)
            locations_get, encodings_get = func.face_process(frame_get)

            if self.fcount % self.frequency == 0:
                try:
                    data_transformed_from_db, crop_imgs, crop_imgs_length, data_transformed_length = func.get_transform_data(frame_get)

                    if data_transformed_length == 0:
                        print('no record in database!')
                    else:
                        for i in range(data_transformed_length):
                            crop_img_encoding = face_recognition.face_encodings(crop_imgs[i])
                            t_count, f_count = func.match_face(data_transformed_from_db[i], crop_img_encoding[0])
                            if t_count == 0:

                                self.db._commit()
                                print('insert one record!')
                            else:
                                print("people exists!")
                except:
                    print('No face or Occur error')


