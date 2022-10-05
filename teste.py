import face_recognition as f
import cv2
import dlib
import numpy as np


predictor = dlib.shape_predictor(
    "classificadores/shape_predictor_68_face_landmarks.dat"
)

img = cv2.imread("test/15.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

classificador_face = cv2.CascadeClassifier(
    "classificadores/haarcascade_frontalface_default.xml"
)
face_encoder = dlib.face_recognition_model_v1(
    "classificadores/dlib_face_recognition_resnet_model_v1.dat"
)


def cv2_to_dlib_rect(cv2_rect):
    return dlib.rectangle(
        cv2_rect[0], cv2_rect[1], cv2_rect[0] + cv2_rect[2], cv2_rect[1] + cv2_rect[3]
    )


faces = classificador_face.detectMultiScale(img_gray, 1.3, 5)

shape = None
face_image = None

if len(faces) > 0:
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        face_image = img[y : y + h, x : x + w]
        face_image = cv2.resize(
            face_image, (200, 200), interpolation=cv2.INTER_LANCZOS4
        )
        dlib_rect = cv2_to_dlib_rect((x, y, w, h))
        shape = predictor(img_gray, dlib_rect)

        for i in range(0, 68):
            cv2.circle(img, (shape.part(i).x, shape.part(i).y), 2, (0, 0, 255), -1)

cv2.imshow("teste", img)
# cv2.waitKey(0)

encodig = np.array(face_encoder.compute_face_descriptor(face_image, shape, 1))
print(encodig)
