import cv2

class CameraHelper:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def check_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if self.cap is None or not self.cap.isOpened():
            print(f"Camera with index {self.camera_index} is not accessible.")
            return False
        else:
            print(f"Camera with index {self.camera_index} is accessible.")
            return True

    def open_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise ValueError(f"Camera with index {self.camera_index} could not be opened.")
        print(f"Camera with index {self.camera_index} opened.")

    def capture_frame(self):
        if self.cap is None or not self.cap.isOpened():
            raise ValueError("Camera is not opened. Call open_camera() before capturing frames.")
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Failed to capture frame from camera.")
        return frame

    def rgb_frame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release_camera(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            print("Camera released.")

    def show_frame(self, frame, window_name='Frame'):
        cv2.imshow(window_name, frame)

    def wait_key(self, delay=1):
        return cv2.waitKey(delay) & 0xFF
