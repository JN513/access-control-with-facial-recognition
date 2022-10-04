import cv2
from os import listdir, path, makedirs
from os.path import isfile, join
import numpy as np

faces_path_treino = "dataset/"  # local onde esta as imagens


def padronizar_imagens(img_caminho):
    imagem = cv2.imread(
        img_caminho, cv2.IMREAD_GRAYSCALE
    )  # ja abre a imagem em escala de cinza
    imagem = cv2.resize(
        imagem, (200, 200), interpolation=cv2.INTER_LANCZOS4
    )  # imagem, tamanho de saida, e interpolação

    return imagem


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
    sujeito = arq[1:2]  # pega o id do sujeito
    sujeitos.append(int(sujeito))  # adiciona a um vetor/lista

sujeitos = np.asarray(sujeitos, dtype=np.int32)  # transforma a lista em um array numpy

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
