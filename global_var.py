import threading
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from ipCam import OnvifCamCtl
import ConfigInit

IP = "192.168.0.8"  # Camera IP address
PORT = 80  # Port
USER = "evg"  # Username
PASS = "Fh1234567890"  # Password

# Globals for threading

ev1 = threading.Event()
ev1.set()

g_frame = None
g_lock = threading.Lock()
g_north = 0
g_pan_range_min = 0
g_pan_range_max = 360
g_tilt_range_min = 0
g_tilt_range_max = 90
g_zoom_range_min = 100
g_zoom_range_max = 31

g_onvif_cam_ip = None#IP
g_onvif_cam_port = None#PORT
g_onvif_cam_user = None#USER
g_onvif_cam_pass = None#PASS

g_rtsp_link = ''

def OnBrightnessValueChange(instance, value):
    cam_ctl.setBrightness(value)
    img_brightness_label.text = "Brightness " + str(round(value, 3))

def OnContrastValueChange(instance, value):
    cam_ctl.setContrast(value)
    img_contrast_label.text = "Contrast " + str(round(value, 3))

conf = ConfigInit.ConfigInit("/home/jin/PycharmProjects/onvif/config.txt")
conf.get_config()

print(g_onvif_cam_ip, g_onvif_cam_port, g_onvif_cam_user, g_onvif_cam_pass)
# Camera
cam_ctl = OnvifCamCtl(g_onvif_cam_ip, g_onvif_cam_port, g_onvif_cam_user, g_onvif_cam_pass)
cam_ctl.connect()
cam_ctl.initPTZ()
cam_ctl.initImageSettingRequest()
cam_ctl.initAbsoluteMoveRequest()
cam_ctl.setIRFilter('AUTO')

pan_input = TextInput(text="0", input_type='number', size_hint_y=None, height=28)
tilt_input = TextInput(text="0", input_type='number', size_hint_y=None, height=28)
zoom_input = TextInput(text="0", input_type='number', size_hint_y=None, height=28)
panTiltBtn = Button(text='Move', size_hint_y=None, height=28, width=50)
zoomBtn = Button(text='Zoom', size_hint_y=None, height=28, width=50)

tp_pan_input = TextInput(text="0", input_type='number', size_hint_y=None, height=28)
tp_tilt_input = TextInput(text="0", input_type='number', size_hint_y=None, height=28)
tp_zoom_input = TextInput(text="0", input_type='number', size_hint_y=None, height=28)
takePositionBtn = Button(text='Take Position', size_hint_y=None, height=28, width=50)

atestPanBtn = Button(text='Full Pan', size_hint_y=None, height=28, width=50)
atestTiltBtn = Button(text='Full Tilt', size_hint_y=None, height=28, width=50)
atestZoomBtn = Button(text='Full Zoom', size_hint_y=None, height=28, width=50)
atestComboBtn = Button(text='Combo Test', size_hint_y=None, height=28, width=50)

t_north_input = TextInput(text="0", input_type='number', size_hint_y=None, height=28)
northBtn = Button(text='Set North', size_hint_y=None, height=28, width=50)

img_setting_bright = Slider(min=0.0, max=100.0, value=30.0)
img_setting_bright.bind(value=OnBrightnessValueChange)
img_setting_contrast = Slider(min=0.0, max=100.0, value=30.0)
img_setting_contrast.bind(value=OnContrastValueChange)
img_contrast_label = Label(text='Contrast ' + str(round(img_setting_contrast.value, 3)), size_hint_y=None, height=15)
img_brightness_label = Label(text='Brightness ' + str(round(img_setting_bright.value, 3)), size_hint_y=None, height=15)
