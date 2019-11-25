from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from camera import Camera
import global_var
from kivy.config import Config
from kivy.core.window import Window
# Config window
Config.set('graphics', 'resizable', '0')

Window.size = (1536, 720)


def pan_tilt_callback(instance):
    print("PanTilt")
    if global_var.pan_input.text.isdigit() and \
            global_var.tilt_input.text.isdigit():
        x = float(global_var.pan_input.text)
        y = float(global_var.tilt_input.text)
        global_var.cam_ctl.move(x, y)


def zoom_callback(instance):
    if global_var.zoom_input.text.isdigit():
        zoom = float(global_var.zoom_input.text)
        global_var.cam_ctl.zoom(zoom)


def take_position_callback(instance):
    if global_var.tp_pan_input.text.isdigit() and \
            global_var.tp_tilt_input.text.isdigit() and \
            global_var.tp_zoom_input.text.isdigit():
        x = float(global_var.tp_pan_input.text)
        y = float(global_var.tp_tilt_input.text)
        z = float(global_var.tp_zoom_input.text)
        global_var.cam_ctl.take_position(x, y, z)


def set_north_callback(instance):
    if global_var.t_north_input.text.isdigit():
        north = float(global_var.t_north_input.text)
        if 0 <= north <= 360:
            global_var.g_north = north


def pan_tilt_layout():
    layout = GridLayout(cols=2, size_hint_y=None, height=110, spacing=5, padding=(10, 5))
    layout.add_widget(Label(text='Pan: ', size_hint_y=None, height=28))
    layout.add_widget(global_var.pan_input)
    layout.add_widget(Label(text='Tilt: ', size_hint_y=None, height=28))
    layout.add_widget(global_var.tilt_input)
    layout.add_widget(Label(text=' ', size_hint_y=None, height=28)) # Stub just to make it more beautiful
    layout.add_widget(global_var.panTiltBtn)
    return layout


def zoom_layout():
    layout = GridLayout(cols=2, size_hint_y=None, height=40, spacing=5, padding=(10, 5))
    layout.add_widget(global_var.zoom_input)
    layout.add_widget(global_var.zoomBtn)
    return layout


def take_position_layout():
    layout = GridLayout(cols=2, size_hint_y=None, height=140, spacing=5, padding=(10, 5))
    layout.add_widget(Label(text='Pan : ', size_hint_y=None, height=15))
    layout.add_widget(global_var.tp_pan_input)
    layout.add_widget(Label(text='Tilt: ', size_hint_y=None, height=15))
    layout.add_widget(global_var.tp_tilt_input)
    layout.add_widget(Label(text='Survey Angle: ', size_hint_y=None, height=15))
    layout.add_widget(global_var.tp_zoom_input)
    layout.add_widget(Label(text=' ', size_hint_y=None, height=28))  # Stub just to make it more beautiful
    layout.add_widget(global_var.takePositionBtn)
    return layout


def autoTestLayout():
    layout = GridLayout(cols=2, size_hint_y=None, height=75, spacing=5, padding=(10, 5))
    layout.add_widget(global_var.atestPanBtn)
    layout.add_widget(global_var.atestTiltBtn)
    layout.add_widget(global_var.atestZoomBtn)
    layout.add_widget(global_var.atestComboBtn)
    return layout


def true_north_Layout():
    layout = GridLayout(cols=2, size_hint_y=None, height=80, spacing=5, padding=(10, 5))
    layout.add_widget(Label(text='North : ', size_hint_y=None, height=15))
    layout.add_widget(global_var.t_north_input)
    layout.add_widget(Label(text=' ', size_hint_y=None, height=28))  # Stub just to make it more beautiful
    layout.add_widget(global_var.northBtn)
    return layout

def image_settings_Layout():
    layout = GridLayout(cols=1, size_hint_y=None, height=100, spacing=5, padding=(10, 5))
    layout.add_widget(global_var.img_brightness_label)
    layout.add_widget(global_var.img_setting_bright)
    layout.add_widget(global_var.img_contrast_label)  # Stub just to make it more beautiful
    layout.add_widget(global_var.img_setting_contrast)
    return layout

def sidebar_layout():
    layout = GridLayout(cols=1, size_hint_y=None, size_hint=(.2, 1))
    layout.add_widget(Label(text='IP Cam Control Panel', size_hint_y=None, height=20))
    layout.add_widget(Label(text='============== North ==============', size_hint_y=None, height=15))
    layout.add_widget(true_north_Layout())
    layout.add_widget(Label(text='======== Pan/Tilt Control  ========', size_hint_y=None, height=15))
    layout.add_widget(Label(text='Pan range  : 0 - 331 degrees.', size_hint_y=None, height=20))
    layout.add_widget(Label(text='Tilt range : 0 - 90 degrees.', size_hint_y=None, height=20))
    layout.add_widget(pan_tilt_layout())
    layout.add_widget(Label(text='========= Zoom Control  =========', size_hint_y=None, height=15))
    layout.add_widget(Label(text='Zoom range : 0.0 - 1.0', size_hint_y=None, height=20))
    layout.add_widget(zoom_layout())
    layout.add_widget(Label(text='========= Take Position =========', size_hint_y=None, height=15))
    layout.add_widget(take_position_layout())
    layout.add_widget(Label(text='=========== Auto Test ===========', size_hint_y=None, height=15))
    layout.add_widget(autoTestLayout())
    layout.add_widget(Label(text='========= Image Settings =========', size_hint_y=None, height=15))
    layout.add_widget(image_settings_Layout())
    return layout



class Gui(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = Camera(fps=25)

    def build(self):
        # root layout layer
        root = FloatLayout()
        # Button handlers
        global_var.panTiltBtn.bind(on_press=pan_tilt_callback)
        global_var.zoomBtn.bind(on_press=zoom_callback)
        global_var.takePositionBtn.bind(on_press=take_position_callback)
        global_var.northBtn.bind(on_press=set_north_callback)
        # video + sidebar layout layer
        layout = BoxLayout(orientation='horizontal', size=(1536, 720))
        layout.add_widget(self.camera)
        layout.add_widget(sidebar_layout())
        root.add_widget(layout)
        return root

    def on_stop(self):
        self.camera.stop()
