import os

DATABASE = "database.db"

URL = "http://localhost:8080/api/token/"
URL_PERFIL = "http://localhost:8080/api/user/getdata/"
URL_LOG = "http://127.0.0.1:8080/api/auth/control/log/"

TOKEN = os.environ.get("TOKEN")

SALA = 1

STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

CLASSIFICADOR_FACE_PATH = "classificadores/haarcascade_frontalface_default.xml"
FACE_RECOGNITION_DLIB_PATH = "classificadores/dlib_face_recognition_resnet_model_v1.dat"
PREDICTOR_DLIB_PATH = "classificadores/shape_predictor_68_face_landmarks.dat"
