import tkinter as tk
from PIL import Image, ImageTk

import supervision as sv
from ultralytics import YOLOv10

from helpers.camera_helper import CameraHelper
# from helpers.serial_helper import SerialHelper
from lib.callback import Log

class App:
    def __init__(self, window, window_title):
        self.model = YOLOv10(f'assets/model/best.pt')
        self.bounding_box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

        self.log = Log()
        self.log.add_log_server()

        self.window = window
        self.window.title(window_title)

        self.camera1 = CameraHelper(0)
        self.camera2 = CameraHelper(1)

        if self.camera1.check_camera():
            self.camera1.open_camera()
        if self.camera2.check_camera():
            self.camera2.open_camera()

        # Create a label widget to display the video feed
        self.video_label = tk.Label(window)
        self.video_label.pack(side=tk.LEFT, padx=10, pady=10)
        # Create a label widget to display the video feed
        self.video_label2 = tk.Label(window)
        self.video_label2.pack(side=tk.LEFT, padx=10, pady=10)

        self.text_label = tk.Label(window, text=f"Good : {self.log.good}" , font=("Arial", 12))
        self.text_label.pack()

        self.text_label = tk.Label(window, text=f"Not Good : {self.log.notGood}" , font=("Arial", 12))
        self.text_label.pack()

        self.update()

    def update(self):
        # Read a frame from the video capture
        frame = self.camera1.capture_frame()
        results = self.model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)

        if 'coca-cola' in detections.data['class_name']:
            self.log.add_log(1)
        # else:
            # self.log.add_log(0)

        annotated_image = self.bounding_box_annotator.annotate(
            scene=frame, detections=detections)
        annotated_image = self.label_annotator.annotate(
            scene=annotated_image, detections=detections)

        # Convert the frame from OpenCV to PIL format
        rgb_frame = self.camera1.rgb_frame(frame)
        pil_img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=pil_img)

        # Update the label with the new frame
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # ######################################################################
        
        # Read a frame from the video capture
        frame2 = self.camera2.capture_frame()
        results2 = self.model(frame2)[0]
        detections2 = sv.Detections.from_ultralytics(results2)

        if 'coca-cola' in detections2.data['class_name']:
            self.log.add_log(1)
        # else:
            # self.log.add_log(0)

        annotated_image2 = self.bounding_box_annotator.annotate(
            scene=frame2, detections=detections2)
        annotated_image2 = self.label_annotator.annotate(
            scene=annotated_image2, detections=detections2)

        # Convert the frame from OpenCV to PIL format
        rgb_frame2 = self.camera2.rgb_frame(frame2)
        pil_img2 = Image.fromarray(rgb_frame2)
        imgtk2 = ImageTk.PhotoImage(image=pil_img2)

        # Update the label with the new frame
        self.video_label2.imgtk = imgtk2
        self.video_label2.configure(image=imgtk2)

        # Schedule the next update
        self.window.after(10, self.update)

    def close(self):
        # Release the video capture and close the Tkinter window
        self.camera1.release_camera()
        self.camera2.release_camera()
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
