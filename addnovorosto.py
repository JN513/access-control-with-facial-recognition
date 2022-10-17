import os
import cv2
import numpy as np
import getpass
from core import padronizar_imagem, padronizar_face
from core.auth import login
from core.models import get_frontal_face_detector

classificador_face = get_frontal_face_detector()

captura_video = cv2.VideoCapture(0)


def main(id):
    # verifica se exite a pasta dataset

    if not os.path.exists("dataset"):
        os.mkdir("dataset")
    if not os.path.exists("dataset_bgr"):
        os.mkdir("dataset_bgr")

    print("Coletando imagens...")

    try:
        contador = 0

        while True:
            captura_ok, frame = captura_video.read()

            if captura_ok:
                frame = padronizar_imagem(frame)
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = classificador_face.detectMultiScale(
                    frame_gray, 1.3, 5
                )  # detecta as faces

                if len(faces) > 0:  # se ele achou uma face
                    contador += 1  # face aumenta mais um

                    if contador <= 10:
                        for (x, y, w, h) in faces:
                            roi = frame_gray[y : y + h, x : x + w]
                            roi = padronizar_face(roi)
                            roi_bgr = frame[y : y + h, x : x + w]
                            roi_bgr = padronizar_face(roi_bgr)
                            cv2.imwrite(
                                "dataset/"
                                + "u"
                                + str(id)
                                + "_"
                                + str(contador)
                                + ".png",
                                roi,
                            )
                            cv2.imwrite(
                                "dataset_bgr/"
                                + "u"
                                + str(id)
                                + "_"
                                + str(contador)
                                + ".png",
                                roi_bgr,
                            )

                        cv2.putText(
                            frame,
                            "Coletado " + str(contador) + " faces",
                            (20, 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 0),
                            2,
                        )  # mostra as faces já coletadas

                    else:  # quando acabar ele fecha
                        cv2.putText(
                            frame,
                            "ConcluIdo",
                            (20, 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 0),
                            2,
                        )
                        captura_video.release()
                        cv2.destroyAllWindows()
                        print("Concluido")
                        break

                for (
                    x,
                    y,
                    w,
                    h,
                ) in faces:  # faz um retangulo mostrando que encontrou o rosto
                    cv2.rectangle(
                        frame, (x, y), (x + w, y + h), (255, 255, 0), 2
                    )  # imagem, extremidades do retangulo, cor, expessuras

                cv2.imshow("janela", frame)

                k = cv2.waitKey(30) & 0xFF  # pega a tecla esc

                if k == 27:  # caso esc for apertado para
                    break

    except KeyboardInterrupt:  # caso de ctrl + c no terminal, tbm para
        captura_video.release()
        cv2.destroyAllWindows()
        print("Interrompido")


if __name__ == "__main__":
    email = input("Email: ")
    password = getpass.getpass("Senha: ")

    login_ok, id, name = login(email, password)

    if login_ok:
        main(id)

        print(f"Imagens Coletadas com sucesso {name}")
    else:
        print("Login falhou")
