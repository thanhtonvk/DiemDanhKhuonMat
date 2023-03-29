import cv2
from unidecode import unidecode

from dal.DiemDanhDal import add_diem_danh
from dal.HocSinhDal import tim_kiem_hoc_sinh
from modules.face_detection import FaceDetection
from modules.face_recognition import FaceRecognition

if __name__ == '__main__':
    face_reg = FaceRecognition()
    face_detection = FaceDetection()
    vid = cv2.VideoCapture(0)
    hoc_sinh = None
    next_frame = 0
    while True:
        ret, frame = vid.read()
        if ret:
            if next_frame % 3 == 0:
                bboxes = face_detection.detect(frame)
                if len(bboxes) > 0:
                    list_hoc_sinh = []
                    for idx, box in enumerate(bboxes):
                        box = list(map(int, box))
                        x_min, y_min, x_max, y_max = box
                        face = frame[y_min:y_max, x_min:x_max]
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 255, 0), 1)
                        if next_frame % 30 == 0:
                            hoc_sinh = tim_kiem_hoc_sinh(face_reg.feature_extractor(face))
                        if hoc_sinh is not None:
                            list_hoc_sinh.append(hoc_sinh)
                    for hoc_sinh in list_hoc_sinh:
                        frame = cv2.putText(frame, unidecode(hoc_sinh.HoTen), (x_min, y_min),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                            (255, 0, 0), 1, cv2.LINE_AA)
                        add_diem_danh(hoc_sinh.Id)
                cv2.imshow('frame', frame)
            next_frame += 1
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
