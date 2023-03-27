import os

import cv2
import numpy as np
import tensorflow as tf

from modules.face_detection import FaceDetection


class FaceRecognition:
    def __init__(self):
        self.interpreter = tf.lite.Interpreter(model_path='model/model_99.tflite')
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()[0]
        self.output_details = self.interpreter.get_output_details()[0]
        self.face_detect = FaceDetection()

    def preprocess(self, np_image: np.ndarray):

        np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
        np_image = cv2.resize(np_image, (128, 128))
        np_image = np_image / 127.5 - 1
        np_image = np.expand_dims(np_image, 0).astype(self.input_details["dtype"])
        return np_image

    def feature_extractor(self, np_image: np.ndarray):
        np_image = self.preprocess(np_image)
        self.interpreter.set_tensor(self.input_details["index"], np_image)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details["index"])[0]
        return output.reshape(1, -1).astype('float')

    def save_face_from_video(self, id_hoc_sinh: int, video: str):
        list_of_faces = []
        list_of_embed = []
        capture = cv2.VideoCapture(video)
        count = 0
        count_frame = 0
        while capture.isOpened():
            # Capture frame-by-frame
            ret, frame = capture.read()
            if ret:
                if count_frame % 15 == 0:
                    boxes = self.face_detect.detect(frame)
                    h, w, _ = frame.shape
                    for idx, box in enumerate(boxes):
                        box = list(map(int, box))
                        x_min, y_min, x_max, y_max = box
                        if x_min < 0:
                            x_min = 0
                        if y_min < 0:
                            y_min = 0
                        if x_max > w:
                            x_max = w
                        if y_max > h:
                            y_max = h
                        face = frame[y_min:y_max, x_min:x_max]
                        try:
                            os.mkdir(f"./faces/{id_hoc_sinh}")
                            cv2.imwrite(f"./faces/{id_hoc_sinh}/{count}.png", face)
                            list_of_faces.append(f"./faces/{id_hoc_sinh}/{count}.png")
                            list_of_embed.append(self.feature_extractor(face))
                            print('create and save face')
                        except:
                            cv2.imwrite(f"./faces/{id_hoc_sinh}/{count}.png", face)
                            list_of_faces.append(f"./faces/{id_hoc_sinh}/{count}.png")
                            list_of_embed.append(self.feature_extractor(face))
                            print('save face')
                        count += 1
            else:
                break
            count_frame += 1
            if count == 3:
                break
        return list_of_faces, list_of_embed

# if __name__ == '__main__':
#     face_reg = FaceRecognition()
#     hocSinh = HocSinh()
#     hocSinh.Id = random.randint(10000, 99999)
#     hocSinh.Lop = 1000
#     hocSinh.HoTen = "Đỗ Thành Tôn"
#     list_of_faces, list_of_embed = face_reg.save_face_from_video(hocSinh.Id, '5782521631881825379.mp4')
#     if len(list_of_faces) == 3:
#         hocSinh.KhuonMat1 = list_of_faces[0]
#         hocSinh.KhuonMat2 = list_of_faces[1]
#         hocSinh.KhuonMat3 = list_of_faces[2]
#         hocSinh.EmbFace1 = list_of_embed[0].tobytes()
#         hocSinh.EmbFace2 = list_of_embed[1].tobytes()
#         hocSinh.EmbFace3 = list_of_embed[2].tobytes()
#     if add(hocSinh):
#         print("ok")
#     else:
#         print('err')
