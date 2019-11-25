import zeep
from onvif import ONVIFCamera
import global_var


def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue


zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

class OnvifCamCtl:
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.cam = None
        self.media = None
        self.media_profile = None
        self.ptz = None
        self.ptz_configuration_options = None
        self.requestA = None
        self.XMAX = 0
        self.XMIN = 0
        self.YMAX = 0
        self.YMIN = 0
        self.ZOOMMIN = 0
        self.ZOOMMAX = 0
        self.xRangeOneDegreePOS = 0.0
        self.yRangeOneDegreePOS = 0.0
        self.xRangeOneDegreeNEG = 0.0
        self.yRangeOneDegreeNEG = 0.0
        self.surveyRangeOneDegree = 0.0
        self.status = None
        self.image = None
        self.image_config = None
        self.image_video_token = None
        self.requestI = None

    def connect(self):
        # Connect to remote camera
        self.cam = ONVIFCamera(self.ip, self.port, self.user, self.password)
        # Create media service object
        self.media = self.cam.create_media_service()



    def initPTZ(self):
        # Create ptz service object
        self.ptz = self.cam.create_ptz_service()
        # Get target profile
        self.media_profile = self.media.GetProfiles()[0]

    def initImageService(self):
        self.image = self.cam.create_imaging_service()
        request = self.image.create_type('GetOptions')
        video_sources = self.cam.media.GetVideoSources()
        self.image_video_token = video_sources[0].token
        request.VideoSourceToken = self.image_video_token
        self.image_config = self.image.GetOptions(request)
        print(self.image_config)

    def initImageSettingRequest(self):
        self.initImageService()
        self.requestI = self.image.create_type('GetImagingSettings')
        self.requestI.VideoSourceToken = self.image_video_token
        self.requestI = self.image.GetImagingSettings(self.requestI)
        self.image.Stop({'VideoSourceToken': self.image_video_token})

    def __interpolateXRangeToDegree(self):
        if self.XMAX == 0 or self.XMIN == 0:
            return False
        middle_bound = global_var.g_pan_range_max / 2
        self.xRangeOneDegreePOS = self.XMAX / middle_bound
        self.xRangeOneDegreeNEG = (self.XMIN * -1) / middle_bound
        return True

    def __interpolateYRangeToDegree(self):
        if self.YMAX == 0 or self.YMIN == 0:
            return False
        middle_bound = global_var.g_tilt_range_max / 2
        self.yRangeOneDegreePOS = self.YMAX / middle_bound
        self.yRangeOneDegreeNEG = (self.YMIN * -1) / middle_bound
        return True

    def __getPanTiltRange(self):
        # Get range of pan and tilt
        self.XMAX = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Max
        self.XMIN = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Min
        self.YMAX = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Max
        self.YMIN = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Min
        self.ZOOMMIN = self.ptz_configuration_options.Spaces.AbsoluteZoomPositionSpace[0].XRange.Min
        self.ZOOMMAX = self.ptz_configuration_options.Spaces.AbsoluteZoomPositionSpace[0].XRange.Max
        self.surveyRangeOneDegree = self.ZOOMMAX / (global_var.g_zoom_range_min - global_var.g_zoom_range_max)

    def __getPTZConfig(self):
        # Get PTZ configuration options for getting absolute move range
        self.requestA = self.ptz.create_type('GetConfigurationOptions')
        self.requestA.ConfigurationToken = self.media_profile.PTZConfiguration.token
        self.ptz_configuration_options = self.ptz.GetConfigurationOptions(self.requestA)
        print(self.ptz)
        self.__getPanTiltRange()
        if not self.__interpolateXRangeToDegree():
            return False
        if not self.__interpolateYRangeToDegree():
            return False
        return True

    def initAbsoluteMoveRequest(self):
        self.__getPTZConfig()
        self.requestA = self.ptz.create_type('AbsoluteMove')
        self.requestA.ProfileToken = self.media_profile.token
        self.ptz.Stop({'ProfileToken': self.media_profile.token})

    #def initImagingSettings(self):

    # Move camera by x - axis
    # g_north - global variable that define
    def __move_x(self, x):
        lower_bound = global_var.g_pan_range_min    # begin of pan range
        middle_bound = global_var.g_pan_range_max / 2   # middle of pan range
        upper_bound = global_var.g_pan_range_max    # end of pan range
        x_mod = (x + global_var.g_north) % upper_bound      # calculate user defined zero position
        if lower_bound <= x_mod <= middle_bound - 1:
            self.requestA.Position.PanTilt.x = x_mod * self.xRangeOneDegreePOS
        elif middle_bound <= x_mod < upper_bound:
            self.requestA.Position.PanTilt.x = ((x_mod - upper_bound) * -1) * self.xRangeOneDegreeNEG * -1

    def __move_y(self, y):
        lower_bound = global_var.g_tilt_range_min   # begin of tilt range
        middle_bound = global_var.g_tilt_range_max / 2  # middle of tilt range
        upper_bound = global_var.g_tilt_range_max   # end of tilt range
        if lower_bound <= y <= middle_bound - 1:
            self.requestA.Position.PanTilt.y = ((y - (middle_bound - 1)) * -1) * self.yRangeOneDegreePOS
        elif middle_bound <= y <= upper_bound:
            self.requestA.Position.PanTilt.y = (y - middle_bound) * self.yRangeOneDegreeNEG * -1

    def __move_zoom(self, zoom):
        z_range = global_var.g_zoom_range_min - global_var.g_zoom_range_max
        if global_var.g_zoom_range_max <= zoom <= global_var.g_zoom_range_min:
            zoom_mod = (((zoom - global_var.g_zoom_range_max) - z_range) * -1) * self.surveyRangeOneDegree
            if zoom_mod > 1:
                zoom_mod = 1
            if zoom_mod < 0:
                zoom_mod = 0
            self.requestA.Position.Zoom.x = zoom_mod

    def move(self, x=0, y=0):
        self.status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        self.requestA.Position = self.status.Position
        self.__move_x(x)
        self.__move_y(y)
        self.ptz.AbsoluteMove(self.requestA)

    def zoom(self, val):
        self.status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        self.requestA.Position = self.status.Position
        self.__move_zoom(val)
        self.ptz.AbsoluteMove(self.requestA)

    def take_position(self, x, y, z):
        self.status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        self.requestA.Position = self.status.Position
        self.__move_x(x)
        self.__move_y(y)
        self.__move_zoom(z)
        self.ptz.AbsoluteMove(self.requestA)

    def setBrightness(self, val):
        request = self.image.create_type('SetImagingSettings')
        request.VideoSourceToken = self.image_video_token
        request.ImagingSettings = {'Brightness': val}
        self.image.SetImagingSettings(request)

    def setContrast(self, val):
        request = self.image.create_type('SetImagingSettings')
        request.VideoSourceToken = self.image_video_token
        request.ImagingSettings = {'Contrast': val}
        self.image.SetImagingSettings(request)

    def setIRFilter(self, val):
        request = self.image.create_type('SetImagingSettings')
        request.VideoSourceToken = self.image_video_token
        request.ImagingSettings = {'IrCutFilter': str(val)}
        self.image.SetImagingSettings(request)

