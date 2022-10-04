from asyncio.windows_events import NULL
import cv2
import numpy as np
import requests
import getpass

URL = "http://localhost:8080/api/token/"
URL_PERFIL = "http://localhost:8080/api/user/getdata/"

classificador_face = cv2.CascadeClassifier(
    "classificadores/haarcascade_frontalface_default.xml"
)

captura_video = cv2.VideoCapture(0)


def padronizar_imagem(img):
    imagem = cv2.resize(
        img, (640, 480), interpolation=cv2.INTER_LANCZOS4
    )  # imagem, tamanho de saida, e interpolação
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    return imagem


def login(email, senha):
    r = requests.post(URL, json={"email": email, "senha": senha})
    if r.status_code != 200:
        return False, NULL

    r = r.json()
    token = r["access"]

    r = requests.get(URL_PERFIL, headers={"Authorization": f"Bearer {token}"})
    if "success" in r.json():
        return True, r.json()["user"]["id"]
    else:
        return False, NULL


def main(id):
    try:
        contador = 0

        while True:
            captura_ok, frame = captura_video.read()

            if captura_ok:
                frame = padronizar_imagem(frame)
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                faces = classificador_face.detectMultiScale(
                    frame_gray, 1.3, 5
                )  # detecta as faces

                if len(faces) > 0:  # se ele achou uma face
                    contador += 1  # face aumenta mais um

                    if contador <= 100:
                        for (x, y, w, h) in faces:
                            roi = frame_gray[y : y + h, x : x + w]
                            cv2.resize(
                                roi, (200, 200), interpolation=cv2.INTER_LANCZOS4
                            )
                            cv2.imwrite(
                                "dataset/"
                                + "u"
                                + str(id)
                                + "_"
                                + str(contador)
                                + ".png",
                                roi,
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

                frame = cv2.cvtColor(
                    frame, cv2.COLOR_RGB2BGR
                )  # opcional, pra cor não ficar bugada
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
    senha = getpass.getpass("Senha: ")

    login_ok, id = login(email, senha)

    if login_ok:
        main(id)
    else:
        print("Login falhou")
