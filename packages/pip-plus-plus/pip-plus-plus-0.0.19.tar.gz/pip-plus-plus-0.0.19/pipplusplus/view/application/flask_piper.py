import logging

from flask import Flask

from pipper.pipper_gen import PipperGenerator
from utils.exceptions import PipRequestException, PipException


class FlaskPipper(Flask):
    def run_command(self, data, req_type=None):
        on_success = "success"
        if data["option"] == "list":
            on_success = "list"
        if not req_type:
            logging.error("Didn't get requst type!")
            raise PipRequestException("Didn't get requst type!")
        if req_type == "POST":
            upgrade_arg = "-U"
            if data["option"] != "install":
                upgrade_arg = ""

            args = {
                "function": data["option"],
                "upgrade": upgrade_arg,
                "package": data["package"]
            }
            proxies = {
                "http": data["http-proxy"],
                "https": data["https-proxy"]
            }

            pipper = PipperGenerator.get_pipper(args=args, proxies=proxies)

            try:
                out = pipper.run_pip()
                return on_success, out
            except PipException as e:
                return "failure", str(e)


