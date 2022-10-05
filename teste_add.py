import cv2
import numpy as np
from core.models import (
    get_frontal_face_detector,
    get_face_recognition_dlib,
    get_shape_predictor_dlib,
)
from core import cv2_to_dlib_rect

classificador_face = get_frontal_face_detector()

face_encoder = get_face_recognition_dlib()

predictor = get_shape_predictor_dlib()

captura_video = cv2.VideoCapture(0)


def main():
    # verifica se exite a pasta dataset

    encodings = []

    print("Coletando imagens...")

    try:
        contador = 0

        while True:
            captura_ok, frame = captura_video.read()

            if captura_ok:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                faces = classificador_face.detectMultiScale(
                    frame_gray, 1.3, 5
                )  # detecta as faces

                if len(faces) > 0:  # se ele achou uma face
                    contador += 1  # face aumenta mais um

                    if contador <= 100:
                        for (x, y, w, h) in faces:
                            roi = frame_gray[y : y + h, x : x + w]
                            roi = cv2.resize(
                                roi, (200, 200), interpolation=cv2.INTER_LANCZOS4
                            )
                            roi_bgr = frame[y : y + h, x : x + w]
                            dlib_rect = cv2_to_dlib_rect((x, y, w, h))
                            shape = predictor(roi, dlib_rect)
                            encodig = np.array(
                                face_encoder.compute_face_descriptor(roi_bgr, shape, 1)
                            )
                            encodings.append(encodig)

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

    return encodings


if __name__ == "__main__":
    encodings = main()

    # print(encodings)

    last = encodings[-1]

    encodings = encodings[:-2]

    r = list(np.linalg.norm(encodings - last, axis=1) <= 0.6)

    print(r)
