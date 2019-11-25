import global_var
import io
import re

class ConfigInit:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_config(self):
        with open(self.file_name) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()
                # print(line)
                if line == '':
                    break
                if line[0] == '#':
                    continue
                line = line.strip('\n')
                param = line.split('=')
                if param[0] == 'onvif_cam_ip':
                    res = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", param[1])
                    if res:
                        global_var.g_onvif_cam_ip = param[1]
                elif param[0] == 'onvif_cam_port':
                    global_var.g_onvif_cam_port = int(param[1])
                elif param[0] == 'onvif_cam_user':
                    global_var.g_onvif_cam_user = param[1]
                elif param[0] == 'onvif_cam_pass':
                    global_var.g_onvif_cam_pass = param[1]
                elif param[0] == 'rtsp_link':
                    global_var.g_rtsp_link = param[1]
                elif param[0] == 'pan_range_min':
                    global_var.g_pan_range_min = int(param[1])
                elif param[0] == 'pan_range_max':
                    global_var.g_pan_range_max = int(param[1])
                elif param[0] == 'tilt_range_min':
                    global_var.g_tilt_range_min = int(param[1])
                elif param[0] == 'tilt_range_max':
                    global_var.g_tilt_range_max = int(param[1])
                elif param[0] == 'zoom_range_min':
                    global_var.g_zoom_range_min = int(param[1])
                elif param[0] == 'zoom_range_max':
                    global_var.g_zoom_range_max = int(param[1])

