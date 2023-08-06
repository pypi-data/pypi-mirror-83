import platform
import sys
from unittest import mock

from pipper.pipper_gen import PipperGenerator


@mock.patch.object(platform, "system", lambda: "Windows")
def test_windows_pipper():
    piper = PipperGenerator.get_pipper(args={"install": True})
    path = piper.pip.replace(" -m pip", "")
    assert path == sys.executable


def test_windows_search_pip():
    if platform.system() == "Windows":
        _ = PipperGenerator.get_pipper(args={"install": True})
    else:
        assert True
