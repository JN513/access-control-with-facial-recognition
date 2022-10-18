import tkinter as tk
import os
import cv2
import dlib
import time
import PIL.Image, PIL.ImageTk
import time
from multiprocessing import Queue
import multiprocessing
import numpy as np
from core.consts import STD_DIMENSIONS
from core.api_client import send_ponto, get_user_by_token
from core.models import get_frontal_face_detector
from pyzbar import pyzbar
from core import padronizar_face
from core.database_manager import get_all
from core.models import (
    get_face_recognition_dlib,
    get_shape_predictor_dlib,
)
from treino import treinar

face_encoder = get_face_recognition_dlib()
predictor = get_shape_predictor_dlib()


class App:
    def __init__(self, window_title, video_source=0):
        # self.window = window

        self.window_title = window_title

        self.atual_window = 0

        self.video_source = video_source

        self.users, self.encodings = get_all()

        self.ok = False
        self.queue = Queue()
        self.delay = 10
        self.id = 0
        self.size = len(self.users)

        self.counter = 0
        self.mode = 0

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)

        if self.atual_window == 0:
            self.window = self.set_auth_screen()

        else:
            self.window = self.set_register_screen()

    def update_encodings(self):
        self.users, self.encodings = get_all()
        self.size = len(self.users)

    def treinar(self):
        self.queue.put("Treinando")

        ok = treinar([self.id])

        if ok:
            self.update_encodings()

            self.queue.put("Treinamento realizado com sucesso")

        else:
            self.queue.put("Treinamento não realizado")

    def snapshot(self):
        # Get a frame from the video source
        ret, frame, _ = self.vid.get_frame()

        if ret:
            cv2.imwrite(
                "snapshots/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
            )

    def check_result(self, queue):
        if not queue.empty():
            self.label_result["text"] = queue.get()
        self.window.after(100, self.check_result, queue)

    def send_ponto(self):

        print("send_ponto")
        status_code, payload = send_ponto(self.id)

        if "success" in payload:
            if payload["success"]:
                print("Ponto registrado")
                self.queue.put(
                    f"Ponto de {payload['tipo']} registrado, {payload['name']} na sala {payload['sala']}"
                )
        else:
            self.queue.put(f"Ponto não registrado, erro: {payload['error']}")

    def baterponto(self):
        roi = self.vid.roi
        roi_bgr = self.vid.roi_bgr

        if self.vid.ok:
            print("Bater Ponto")

            if len(self.users) == 0:
                self.queue.put("Usuario não Cadastrado ou sem acesso.")
                return

            dlib_react = dlib.rectangle(0, 0, 200, 200)

            shape = predictor(roi, dlib_react)

            encoding = np.array(face_encoder.compute_face_descriptor(roi_bgr, shape, 1))

            r = list(np.linalg.norm(self.encodings - encoding, axis=1) <= 0.6)

            for i in range(self.size):
                if r[i]:
                    self.id = self.users[i]
                    break

            if self.id != 0:
                self.t1 = multiprocessing.Process(target=self.send_ponto, args=())
                self.t1.start()

            else:
                self.queue.put("Usuario não Cadastrado ou sem acesso")

    def update(self):
        ret, frame, data = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.mode == 1 and data != "":
            self.label_result["text"] = "Obtendo Usuario"

            status_code, payload = get_user_by_token(data)

            if "success" in payload and status_code != 400:
                if payload["success"]:
                    self.queue.put("Usuario Autenticado com sucesso")
                    self.mode = 2
                    self.vid.atual = 0
                    self.counter = 1
                    self.id = payload["user_id"]
                    if not os.path.exists("dataset"):
                        os.mkdir("dataset")
                    if not os.path.exists("dataset_bgr"):
                        os.mkdir("dataset_bgr")
                else:
                    self.mode = 0
                    self.id = 0
                    self.queue.put(
                        f"Erro ao autenticar Usuario, erro: {payload['error']}"
                    )
                    self.voltar()
                    # self.after = self.window.after(self.delay, self.update)

            else:
                # self.after = self.window.after(self.delay, self.update)

                self.mode = 0
                self.id = 0
                self.queue.put(f"Erro ao autenticar Usuario")
                self.voltar()
        elif self.mode == 2:
            if self.counter <= 10:

                roi = self.vid.roi
                roi_bgr = self.vid.roi_bgr

                if self.vid.ok:

                    cv2.imwrite(
                        "dataset/"
                        + "u"
                        + str(self.id)
                        + "_"
                        + str(self.counter)
                        + ".png",
                        roi,
                    )
                    cv2.imwrite(
                        "dataset_bgr/"
                        + "u"
                        + str(self.id)
                        + "_"
                        + str(self.counter)
                        + ".png",
                        roi_bgr,
                    )

                    self.counter += 1
            else:
                self.t2 = multiprocessing.Process(target=self.treinar, args=())
                self.t2.start()

                self.mode = 0
                self.id = 0
                self.queue.put(
                    "Usuario cadastrado com sucesso, aguarde alguns instantes para as alterações serem aplicadas."
                )

                self.voltar()

        if self.mode != 2:
            self.after = self.window.after(self.delay, self.update)
        else:
            self.after = self.window.after(15, self.update)

    def set_auth_screen(self):
        window_auth = tk.Tk()

        window_auth.title(self.window_title)

        top_title = tk.Label(
            window_auth,
            text="Sistema de Reconhecimento Facial",
            font=("Helvetica", 16),
            background="black",
            foreground="white",
        )
        top_title.pack(fill=tk.X)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(
            window_auth, width=self.vid.width, height=self.vid.height
        )
        self.canvas.pack()

        footer_frame = tk.Frame(window_auth, background="black")
        footer_frame.pack(fill=tk.X)

        # Button that lets the user take a snapshot
        btn_snapshot = tk.Button(
            footer_frame,
            text="Snapshot",
            command=self.snapshot,
            background="blue",
            foreground="white",
        )
        btn_snapshot.pack(fill=tk.X)

        btn_btp = tk.Button(
            footer_frame,
            text="Bater Ponto",
            command=self.baterponto,
            background="green",
            foreground="white",
        )
        btn_btp.pack(fill=tk.X)

        btn_stop = tk.Button(
            footer_frame,
            text="Cadastrar",
            command=self.cadastrar,
            background="black",
            foreground="white",
        )
        btn_stop.pack(fill=tk.X)

        # quit button
        btn_quit = tk.Button(
            footer_frame,
            text="QUIT",
            command=quit,
            background="red",
            foreground="white",
        )
        btn_quit.pack(fill=tk.X)

        self.label_result = tk.Label(
            footer_frame,
            text="Resultado",
            background="black",
            foreground="white",
            font=("Helvetica", 16),
        )
        self.label_result.pack(fill=tk.X)

        # After it is called once, the update method will be automatically called every delay milliseconds

        window_auth.after(100, self.check_result, self.queue)

        self.window = window_auth

        self.update()

        self.window.mainloop()

    def set_register_screen(self):
        window_register = tk.Tk()

        window_register.title(self.window_title)

        top_title = tk.Label(
            window_register,
            text="Sistema de Reconhecimento Facial",
            font=("Helvetica", 16),
            background="black",
            foreground="white",
        )
        top_title.pack(fill=tk.X)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(
            window_register, width=self.vid.width, height=self.vid.height
        )
        self.canvas.pack()

        footer_frame = tk.Frame(window_register, background="black")
        footer_frame.pack(fill=tk.X)

        btn_stop = tk.Button(
            footer_frame,
            text="Voltar",
            command=self.voltar,
            background="black",
            foreground="white",
        )
        btn_stop.pack(fill=tk.X)

        # quit button
        btn_quit = tk.Button(
            footer_frame,
            text="QUIT",
            command=quit,
            background="red",
            foreground="white",
        )
        btn_quit.pack(fill=tk.X)

        self.label_result = tk.Label(
            footer_frame,
            text="Aponte o QRCode para a camera",
            background="black",
            foreground="white",
            font=("Helvetica", 16),
        )
        self.label_result.pack(fill=tk.X)

        window_register.after(100, self.check_result, self.queue)

        self.window = window_register

        self.update()

        self.window.mainloop()

    def cadastrar(self):
        self.window.destroy()
        self.atual_window = 1
        self.mode = 1
        self.vid.atual = 1
        self.set_register_screen()

    def voltar(self):
        self.window.destroy()
        self.atual_window = 0
        self.mode = 0
        self.vid.atual = 0
        self.set_auth_screen()


class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.classificador_face = get_frontal_face_detector()

        self.atual = 0

        self.roi_bgr = None
        self.roi = None
        self.ok = False

        self.vid = cv2.VideoCapture(video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        res = STD_DIMENSIONS["480p"]

        # set video sourec width and height
        self.vid.set(3, res[0])
        self.vid.set(4, res[1])

        # Get video source width and height
        self.width, self.height = res

    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                custom_data = ""

                if not self.atual:
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                    faces = self.classificador_face.detectMultiScale(frame_gray, 1.3, 5)

                    if len(faces) > 0:
                        for (x, y, w, h) in faces:
                            cv2.rectangle(
                                frame, (x, y), (x + w, y + h), (255, 255, 0), 2
                            )
                            self.roi = frame_gray[y : y + h, x : x + w]
                            self.roi = padronizar_face(self.roi)
                            self.roi_bgr = frame[y : y + h, x : x + w]
                            self.roi_bgr = padronizar_face(self.roi_bgr)

                            self.ok = True
                    else:
                        self.roi_bgr = None
                        self.roi = None
                        self.ok = False

                else:
                    self.roi_bgr = None
                    self.roi = None
                    self.ok = False

                    qrcodes = pyzbar.decode(frame)

                    for qrcode in qrcodes:
                        (x, y, w, h) = qrcode.rect
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        custom_data = qrcode.data.decode("utf-8")

                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), custom_data)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()


def main():
    # Create a window and pass it to the Application object
    App("Ponto Labsoft")


main()
