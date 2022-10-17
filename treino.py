import cv2
from os import listdir, path, makedirs
from os.path import isfile, join
import numpy as np
import dlib
from core.models import (
    get_face_recognition_dlib,
    get_shape_predictor_dlib,
)
from core.database_manager import insert_array, delete_from_user, insert_data_alter

faces_path_treino = "dataset/"  # local onde esta as imagens
faces_path_treino_bgr = "dataset_bgr/"  # local onde esta as imagens

face_encoder = get_face_recognition_dlib()

predictor = get_shape_predictor_dlib()


def padronizar_imagens(img_caminho):
    imagem = cv2.imread(
        img_caminho, cv2.IMREAD_GRAYSCALE
    )  # ja abre a imagem em escala de cinza
    imagem = cv2.resize(
        imagem, (200, 200), interpolation=cv2.INTER_LANCZOS4
    )  # imagem, tamanho de saida, e interpolação

    return imagem


def padronizar_imagens_bgr(img_caminho):
    imagem = cv2.imread(img_caminho)  # ja abre a imagem em escala de cinza
    imagem = cv2.resize(
        imagem, (200, 200), interpolation=cv2.INTER_LANCZOS4
    )  # imagem, tamanho de saida, e interpolação

    return imagem


def treinar(users_ids: list):

    for user_id in users_ids:
        delete_from_user(user_id)
        insert_data_alter(user_id)

    lista_faces_treino_bgr = [
        f
        for f in listdir(faces_path_treino_bgr)
        if isfile(join(faces_path_treino_bgr, f))
    ]

    sujeitos_bgr = []
    imagens_bgr = []

    for i, arq in enumerate(
        lista_faces_treino_bgr
    ):  # padroniza a imagem e add a lista de dados de treinamento
        sujeito = int(arq.split("_")[0][1:])

        if sujeito in users_ids:
            img_path = faces_path_treino_bgr + arq
            imagem = padronizar_imagens(img_path)
            imagens_bgr.append(imagem)
            sujeitos_bgr.append(sujeito)  # adiciona a um vetor/lista
        else:
            continue

    for i, image in enumerate(imagens_bgr):
        dlib_react = dlib.rectangle(0, 0, 200, 200)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        roi_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        shape = predictor(roi_gray, dlib_react)

        encoding = np.array(face_encoder.compute_face_descriptor(image, shape, 1))

        insert_array(sujeitos_bgr[i], encoding)


if __name__ == "__main__":
    treinar()
