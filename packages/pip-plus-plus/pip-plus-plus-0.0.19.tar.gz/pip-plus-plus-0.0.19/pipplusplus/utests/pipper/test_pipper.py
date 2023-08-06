import platform
import sys

from pipper.pipper_gen import PipperGenerator


def test_windows_pipper():
    if platform.system() == "Windows":
        piper = PipperGenerator.get_pipper(args={"install": True})
        path = piper.pip[0]
        assert path == sys.executable
    else:
        True


def test_windows_search_pip():
    if platform.system() == "Windows":
        _ = PipperGenerator.get_pipper(args={"install": True})
    else:
        assert True


def test_linux_search_pip():
    if platform.system() == "Linux":
        _ = PipperGenerator.get_pipper(args={"install": True})
    else:
        assert True
