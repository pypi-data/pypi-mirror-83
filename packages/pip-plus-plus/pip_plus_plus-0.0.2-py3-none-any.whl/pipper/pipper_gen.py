import platform

from pipper.pipper_main import PipperWindows, PipperLinux


class PipperGenerator(object):
    PIPPERS = {
        "Windows": PipperWindows,
        "Linux": PipperLinux
    }

    @classmethod
    def get_pipper(cls, **kwargs):
        curr_system = platform.system()
        return PipperGenerator.PIPPERS[curr_system](**kwargs)
