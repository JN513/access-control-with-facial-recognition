import cv2
from os import listdir, path, makedirs
from os.path import isfile, join
import numpy as np
import dlib
from core.models import (
    get_face_recognition_dlib,
    get_shape_predictor_dlib,
)
from core.database_manager import insert_array

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
    imagem = cv2.imread(img_caminhom)  # ja abre a imagem em escala de cinza
    imagem = cv2.resize(
        imagem, (200, 200), interpolation=cv2.INTER_LANCZOS4
    )  # imagem, tamanho de saida, e interpolação

    return imagem


def treinar():
    lista_faces_treino = [
        f for f in listdir(faces_path_treino) if isfile(join(faces_path_treino, f))
    ]  # pega todas as imagens do diretorio de treino

    dados_treinamento, sujeitos = [], []

    for i, arq in enumerate(
        lista_faces_treino
    ):  # padroniza a imagem e add a lista de dados de treinamento
        img_path = faces_path_treino + arq
        imagem = padronizar_imagens(img_path)
        dados_treinamento.append(imagem)
        sujeito = arq.split("_")[0][1:]
        sujeitos.append(int(sujeito))  # adiciona a um vetor/lista

    sujeitos = np.asarray(
        sujeitos, dtype=np.int32
    )  # transforma a lista em um array numpy

    print("Treinando...")

    print("LBPH... ", end="")

    model_lbph = cv2.face.LBPHFaceRecognizer_create(1, 1, 7, 7)
    model_lbph.train(dados_treinamento, sujeitos)
    print("OK")
    model_lbph.save("classificadores/lbph_trainigdata.xml")

    print("Modelo LBPH, gerado e salvo.")

    print("Eigenface... ", end="")

    model_eigenface = cv2.face.EigenFaceRecognizer_create(15)
    model_eigenface.train(dados_treinamento, sujeitos)
    print("OK")
    model_eigenface.save("classificadores/eigenface_trainigdata.xml")

    print("Modelo Eigenface, gerado e salvo.")

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
        img_path = faces_path_treino_bgr + arq
        imagem = padronizar_imagens(img_path)
        imagens_bgr.append(imagem)

        sujeito = arq.split("_")[0][1:]

        sujeitos_bgr.append(int(sujeito))  # adiciona a um vetor/lista

    for i, image in enumerate(imagens_bgr):
        dlib_react = dlib.rectangle(0, 0, 200, 200)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        roi_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        shape = predictor(roi_gray, dlib_react)

        encoding = np.array(face_encoder.compute_face_descriptor(image, shape, 1))

        insert_array(sujeitos_bgr[i], encoding)


if __name__ == "__main__":
    treinar()
