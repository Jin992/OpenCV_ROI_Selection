import cv2
import threading
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import global_var


def camReader(rtsp):
    cap = cv2.VideoCapture(rtsp)
    while cap.isOpened():
        try:
            if not global_var.ev1.wait(0):
                break
            ret, frame = cap.read()
            if ret:
                global_var.g_lock.acquire()
                global_var.g_frame = frame
                global_var.g_lock.release()
        except cv2.error as err:
            print(err)
            break
    cap.release()


class Camera(Image):
    def __init__(self, fps, **kwargs):
        super(Camera, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.opencv_thread = threading.Thread(target=camReader,
                                              args=(global_var.g_rtsp_link, ))
        self.opencv_thread.daemon = True
        self.opencv_thread.start()

    def update(self, dt):
        global_var.g_lock.acquire()
        frame = global_var.g_frame
        global_var.g_lock.release()
        if frame is None:
            return
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture

    def stop(self):
        global_var.ev1.clear()
        if self.opencv_thread.isAlive():
            self.opencv_thread.join()
