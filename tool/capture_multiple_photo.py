import cv2
import tkinter as tk
from tkinter import Button, Label, Checkbutton, IntVar
from PIL import Image, ImageTk
import datetime

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.available_cameras = self.detect_cameras()
        if not self.available_cameras:
            print("No cameras detected. Please check your connections.")
            return

        self.selected_cameras = []

        self.check_vars = [IntVar() for _ in self.available_cameras]
        self.checkbuttons = [Checkbutton(window, text=f"Camera {i+1}", variable=self.check_vars[i])
                             for i in range(len(self.available_cameras))]
        for i, checkbutton in enumerate(self.checkbuttons):
            checkbutton.grid(row=0, column=i)

        self.btn_capture = Button(window, text="Capture", width=10, command=self.capture_images)
        self.btn_capture.grid(row=1, columnspan=len(self.available_cameras))

        self.btn_start = Button(window, text="Start", width=10, command=self.start_cameras)
        self.btn_start.grid(row=2, columnspan=len(self.available_cameras))

        self.labels = []
        self.caps = []
        self.frames = []
        self.photos = []

        self.window.mainloop()

    def detect_cameras(self):
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            # if not cap.read()[0]:
            if not cap.isOpened():
                cap.release()
                break
            else:
                print(f"Camera {index} detected")
                arr.append(index)
            cap.release()
            index += 1
        return arr

    def start_cameras(self):
        self.selected_cameras = [index for index, var in enumerate(self.check_vars) if var.get() == 1]
        if not self.selected_cameras:
            print("No cameras selected!")
            return

        self.caps = [cv2.VideoCapture(i) for i in self.selected_cameras]
        self.frames = [None] * len(self.caps)
        self.photos = [None] * len(self.caps)

        for widget in self.window.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        self.labels = [Label(self.window) for _ in self.caps]
        for i, label in enumerate(self.labels):
            label.grid(row=2, column=i)

        self.update()

    def update(self):
        for i, cap in enumerate(self.caps):
            ret, frame = cap.read()
            if ret:
                self.frames[i] = frame
                self.photos[i] = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.labels[i].config(image=self.photos[i])

        self.window.after(10, self.update)

    def capture_images(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for i, frame in enumerate(self.frames):
            if frame is not None:
                filename = f'captured_image_camera_{self.selected_cameras[i]+1}_{timestamp}.jpg'
                cv2.imwrite(filename, frame)
                print(f"Image saved as '{filename}'")

    def __del__(self):
        for cap in self.caps:
            if cap.isOpened():
                cap.release()

# Create a window and pass it to the CameraApp class
root = tk.Tk()
app = CameraApp(root, "Multi-Camera App")
