import cv2
import dlib
from core.consts import (
    CLASSIFICADOR_FACE_PATH,
    FACE_RECOGNITION_DLIB_PATH,
    PREDICTOR_DLIB_PATH,
)


def get_frontal_face_detector():
    return cv2.CascadeClassifier(CLASSIFICADOR_FACE_PATH)


def get_face_recognition_dlib():
    return dlib.face_recognition_model_v1(FACE_RECOGNITION_DLIB_PATH)


def get_shape_predictor_dlib():
    return dlib.shape_predictor(PREDICTOR_DLIB_PATH)
