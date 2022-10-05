import imp
import cv2
import dlib
import numpy as np


def padronizar_imagem(img):
    img = cv2.resize(
        img, (640, 480), interpolation=cv2.INTER_LANCZOS4
    )  # imagem, tamanho de saida, e interpolação
    return img


def padronizar_face(img):
    img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_LANCZOS4)
    return img


def cv2_to_dlib_rect(cv2_rect):
    return dlib.rectangle(
        cv2_rect[0], cv2_rect[1], cv2_rect[0] + cv2_rect[2], cv2_rect[1] + cv2_rect[3]
    )
