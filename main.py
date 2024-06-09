import tkinter as tk
from PIL import Image, ImageTk

import supervision as sv
from ultralytics import YOLOv10

from helpers.camera_helper import CameraHelper
# from helpers.serial_helper import SerialHelper
from helpers.database.sqlite_helper import SQLiteHelper

class App:
    def __init__(self, window, window_title):
        self.model = YOLOv10(f'assets/model/best.pt')
        self.bounding_box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

        self.sqlite = SQLiteHelper("assets/databases/log.db")
        self.sqlite.connect()

        self.window = window
        self.window.title(window_title)

        self.camera_helper = CameraHelper()

        if self.camera_helper.check_camera():
            self.camera_helper.open_camera()

        # Create a label widget to display the video feed
        self.video_label = tk.Label(window)
        self.video_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.text_label = tk.Label(window, text="Hello World", font=("Arial", 12))
        self.text_label.pack(side=tk.RIGHT, padx=10, pady=10)

        self.update()

    def update(self):
        # Read a frame from the video capture
        frame = self.camera_helper.capture_frame()
        results = self.model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)

        annotated_image = self.bounding_box_annotator.annotate(
            scene=frame, detections=detections)
        annotated_image = self.label_annotator.annotate(
            scene=annotated_image, detections=detections)

        # Convert the frame from OpenCV to PIL format
        rgb_frame = self.camera_helper.rgb_frame(frame)
        pil_img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=pil_img)

        # Update the label with the new frame
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Schedule the next update
        self.window.after(10, self.update)

    def close(self):
        # Release the video capture and close the Tkinter window
        self.camera_helper.release_camera()
        self.window.destroy()

def main():
    # Create a Tkinter window
    window = tk.Tk()

    # Set the window size
    window.attributes("-fullscreen", True)

    # Create the application
    app = App(window, "QC")

    # Run the Tkinter event loop
    window.mainloop()

    # Close the video capture when the window is closed
    app.close()

if __name__ == "__main__":
    main()
