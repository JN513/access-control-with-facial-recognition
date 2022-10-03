import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import datetime as dt
import argparse


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.ok = False

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
        self.delay = 10
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite(
                "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
            )

    def baterponto(self):
        print("Bater Ponto")

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
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # 1. Video Type
        VIDEO_TYPE = {
            "avi": cv2.VideoWriter_fourcc(*"XVID"),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            "mp4": cv2.VideoWriter_fourcc(*"XVID"),
        }

        self.fourcc = VIDEO_TYPE["mp4"]

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

    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                faces = self.classificador_face.detectMultiScale(frame_gray, 1.3, 5)
                for (
                    x,
                    y,
                    w,
                    h,
                ) in faces:  # faz um retangulo mostrando que encontrou o rosto
                    cv2.rectangle(
                        frame, (x, y), (x + w, y + h), (255, 255, 0), 2
                    )  # imagem, extremidades do retangulo, cor, expessuras
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
