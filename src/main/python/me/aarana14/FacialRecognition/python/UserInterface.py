from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2


class Facial_RecognitionApp(App):
    def __init__(self, ret, frame):
        App.__init__(self)
        # self.capture = capture
        self.setNewFrame(ret, frame)
        print("UI Done")

    def build(self):
        self.layout = BoxLayout(orientation="vertical")
        self.image = Image()
        self.layout.add_widget(self.image)
        self.layout.add_widget(Button(
            text = "Click Here",
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            size_hint = (None, None))
        )
        # self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/60.0)
        return self.layout

    def load_video(self, *args):
        # ret, self.frame = self.capture.read()
        self.image_frame = self.frame
        buffer = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.image.texture = texture

    def setNewFrame(self, ret, frame):
        self.ret = ret
        self.frame = frame
        # print("Updated")
    
