from webcam.__init__ import *
import func

class Camera2():
    def __init__(self,video_capture):
        self.video_caputre = video_capture
        self.fcount = config['frequency_count']
        self.frequency = config['frequency']
        self.crop_face_dir = config['crop_image_dir']

    def cam2(self):
        while True:
            frame_judge, rgb_frame_judge = func.Video(self.video_capture)
            locations_get, encodings_get = func.FaceProcess(frame_judge)

            if self.fcount % self.frequency == 0:
                exist_images = os.listdir(self.crop_face_dir)
                crop_imgs = func.CropFace(frame_judge)
                crop_imgs_length = len(crop_imgs)

                for crop_img in crop_imgs:
                    for old_image in exist_images:
                        true, false = func.MatchFace(old_image, crop_img)
                        if true > 0:
                            pass


