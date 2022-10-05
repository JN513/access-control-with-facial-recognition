import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
from multiprocessing import Queue
import multiprocessing
import requests
import os
import datetime

SALA = 1  # ID da sala na API
token = os.environ.get("TOKEN")
URL = "http://127.0.0.1:8080/api/auth/control/log/"


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.ok = False
        self.queue = Queue()

        self.top_title = tk.Label(
            window,
            text="Sistema de Reconhecimento Facial",
            font=("Helvetica", 16),
            background="black",
            foreground="white",
        )
        self.top_title.pack(fill=tk.X)

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.footer_frame = tk.Frame(window, background="black")
        self.footer_frame.pack(fill=tk.X)

        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(
            self.footer_frame,
            text="Snapshot",
            command=self.snapshot,
            background="blue",
            foreground="white",
        )
        self.btn_snapshot.pack(fill=tk.X)

        self.btn_btp = tk.Button(
            self.footer_frame,
            text="Bater Ponto",
            command=self.baterponto,
            background="green",
            foreground="white",
        )
        self.btn_btp.pack(fill=tk.X)

        self.btn_stop = tk.Button(
            self.footer_frame,
            text="Cadastrar",
            command=self.cadastrar,
            background="black",
            foreground="white",
        )
        self.btn_stop.pack(fill=tk.X)

        # quit button
        self.btn_quit = tk.Button(
            self.footer_frame,
            text="QUIT",
            command=quit,
            background="red",
            foreground="white",
        )
        self.btn_quit.pack(fill=tk.X)

        self.label_result = tk.Label(
            self.footer_frame,
            text="Resultado",
            background="black",
            foreground="white",
            font=("Helvetica", 16),
        )
        self.label_result.pack(fill=tk.X)

        # After it is called once, the update method will be automatically called every delay milliseconds

        self.window.after(100, self.check_result, self.queue)
        self.delay = 10
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

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
        data = {"id": self.vid.id, "sala": SALA}
        r = requests.post(
            URL,
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {token}",
            },
        )

        r = r.json()

        if "success" in r:
            if r["success"]:
                print("Ponto registrado")
                self.queue.put(
                    f"Ponto de {r['tipo']} registrado, {r['name']} na sala {r['sala']}"
                )
        else:
            self.queue.put(f"Ponto não registrado, erro: {r['error']}")

    def baterponto(self):
        id = self.vid.get_id()
        if id != 0:
            print("Bater Ponto")

            self.t1 = multiprocessing.Process(target=self.send_ponto, args=())
            self.t1.start()

            self.vid.id = 0

    def cadastrar(self):
        ...

    def update(self):

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        # if self.ok:
        #    self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)


class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.classificador_face = cv2.CascadeClassifier(
            "classificadores/haarcascade_frontalface_default.xml"
        )
        self.model_lbph = cv2.face.LBPHFaceRecognizer_create(2, 2, 7, 7, 15)
        self.model_lbph.read("classificadores/lbph_trainigdata.xml")
        self.id = 0

        self.vid = cv2.VideoCapture(video_source)
        self.counter = 0

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # 2. Video Dimension
        STD_DIMENSIONS = {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        res = STD_DIMENSIONS["480p"]

        # set video sourec width and height
        self.vid.set(3, res[0])
        self.vid.set(4, res[1])

        # Get video source width and height
        self.width, self.height = res

    def get_id(self):
        return self.id

    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                faces = self.classificador_face.detectMultiScale(frame_gray, 1.3, 5)

                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                        roi = frame_gray[y : y + h, x : x + w]
                        roi = cv2.resize(
                            roi, (200, 200), interpolation=cv2.INTER_LANCZOS4
                        )
                        predicao = self.model_lbph.predict(roi)
                        cv2.putText(
                            frame,
                            f"Similaridade: {round(predicao[1], 2)} user: {predicao[0]}",
                            (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 0),
                            2,
                        )
                        if predicao[1] < 4.0:
                            self.id = predicao[0]
                else:
                    self.id = 0

                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
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
    App(tk.Tk(), "Video Recorder")


main()
