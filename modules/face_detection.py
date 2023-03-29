import cv2
import numpy as np

from yoloface.face_detector import YoloDetector


class FaceDetection:
    def __init__(self):
        self.model = YoloDetector(target_size=640, device="cpu",
                                  min_face=20)

    def detect(self, np_image: np.ndarray):
        np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
        boxes, _ = self.model.predict(np_image)
        return boxes[0]


# if __name__ == '__main__':
#     face_detection = FaceDetection()
#     vid = cv2.VideoCapture('5782521631881825379.mp4')
#     while True:
#         ret, frame = vid.read()
#         bboxes = face_detection.detect(frame)
#         if len(bboxes) > 0:
#             for idx, box in enumerate(bboxes):
#                 box = list(map(int, box[0]))
#                 x_min, y_min, x_max, y_max = box
#                 cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 255, 0), 1)
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     # After the loop release the cap object
#     vid.release()
#     # Destroy all the windows
#     cv2.destroyAllWindows()
