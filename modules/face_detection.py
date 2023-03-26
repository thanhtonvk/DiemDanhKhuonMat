from yoloface.face_detector import YoloDetector
import cv2

if __name__ == '__main__':
    model = YoloDetector(target_size=320, device="cpu",
                         min_face=90)
    vid = cv2.VideoCapture('../Data/1148048998748956945.mp4')
    while True:
        ret, frame = vid.read()
        bboxes, points = model.predict(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if len(bboxes) > 0:
            for idx, box in enumerate(bboxes):
                box = list(map(int, box[0]))
                x_min, y_min, x_max, y_max = box
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 255, 0), 1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
