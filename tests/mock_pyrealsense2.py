import enum

import numpy as np


class RSStream(enum.Enum):
    color = 0
    depth = 1


class RSFormat(enum.Enum):
    rgb8 = 0
    z16 = 1


class RSConfig:
    def enable_device(self, device_id: str):
        self.device_enabled = device_id

    def enable_stream(
        self, stream_type: RSStream, width=None, height=None, color_format: RSFormat = None, fps=None
    ):
        self.stream_type = stream_type
        # Overwrite default values when possible
        self.width = 848 if width is None else width
        self.height = 480 if height is None else height
        self.color_format = RSFormat.rgb8 if color_format is None else color_format
        self.fps = 30 if fps is None else fps


class RSColorProfile:
    def __init__(self, config: RSConfig):
        self.config = config

    def fps(self):
        return self.config.fps

    def width(self):
        return self.config.width

    def height(self):
        return self.config.height


class RSColorStream:
    def __init__(self, config: RSConfig):
        self.config = config

    def as_video_stream_profile(self):
        return RSColorProfile(self.config)


class RSProfile:
    def __init__(self, config: RSConfig):
        self.config = config

    def get_stream(self, color_format: RSFormat):
        del color_format  # unused
        return RSColorStream(self.config)


class RSPipeline:
    def __init__(self):
        self.started = False
        self.config = None

    def start(self, config: RSConfig):
        self.started = True
        self.config = config
        return RSProfile(self.config)

    def stop(self):
        if not self.started:
            raise RuntimeError("You need to start the camera before stop.")
        self.started = False
        self.config = None

    def wait_for_frames(self, timeout_ms=50000):
        del timeout_ms  # unused
        return RSFrames(self.config)


class RSFrames:
    def __init__(self, config: RSConfig):
        self.config = config

    def get_color_frame(self):
        return RSColorFrame(self.config)

    def get_depth_frame(self):
        return RSDepthFrame(self.config)


class RSColorFrame:
    def __init__(self, config: RSConfig):
        self.config = config

    def get_data(self):
        data = np.ones((self.config.height, self.config.width, 3), dtype=np.uint8)
        # Create a difference between rgb and bgr
        data[:, :, 0] = 2
        return data


class RSDepthFrame:
    def __init__(self, config: RSConfig):
        self.config = config

    def get_data(self):
        return np.ones((self.config.height, self.config.width), dtype=np.uint16)


class RSDevice:
    def __init__(self):
        pass

    def get_info(self, camera_info) -> str:
        del camera_info  # unused
        # return fake serial number
        return "123456789"


class RSContext:
    def __init__(self):
        pass

    def query_devices(self):
        return [RSDevice()]


class RSCameraInfo:
    def __init__(self, serial_number):
        del serial_number
        pass