import logging
import subprocess

from utils.Validator import UrlValidator
from utils.exceptions import PipProxyException, PipUrlException


class ProxySetter(object):
    SET_COMMANDS = {
        "linux": "export",
        "windows": "set"
    }

    def __init__(self, os):
        self.set_command = ProxySetter.SET_COMMANDS[os.lower()]

    def set(self, proxies):
        http = proxies["http"]
        https = proxies["https"]
        url_validator = UrlValidator()
        err = ""
        if not url_validator.valid(http) and http:
            err += f"The http url is invalid: {http}"

        if not url_validator.valid(https) and http:
            if err:
                err += "\n"
            err += f"The https url is invalid: {https}"

        if err:
            raise PipUrlException(err)

        if http:
            p = subprocess.run([self.set_command, f"http_proxy={http}"])
            if p.returncode:
                logging.error(f"Failed to set http proxy {http}")
                raise PipProxyException(f"Failed to set http proxy {http}")
        if http:
            p = subprocess.run([self.set_command, f"https_proxy={https}"])
            if p.returncode:
                logging.error(f"Failed to set http proxy {https}")
                raise PipProxyException(f"Failed to set http proxy {https}")
