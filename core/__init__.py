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
