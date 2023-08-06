from unittest import mock
from unittest.mock import MagicMock

import pytest
from pytest import fixture

from utils.exceptions import PipUrlException
from utils.proxy.proxy_setters import ProxySetter


@fixture
def proxies():
    return {
        "http": "http://mock.com",
        "https": "https://mock.com"
    }


@fixture
def bad_proxies():
    return {
        "http": "httpssss://mock.com",
        "https": "https://mock"
    }


@fixture
def process_mock():
    p = MagicMock()
    p.returncode = 0
    return p


@mock.patch("utils.proxy.proxy_setters.subprocess.run")
def test_set_success(subprocess_run_mock, proxies, process_mock):
    subprocess_run_mock.return_value = process_mock
    proxy_setter = ProxySetter("windows")
    proxy_setter.set(proxies)


@mock.patch("utils.proxy.proxy_setters.subprocess.run")
def test_set_failed(subprocess_run_mock, bad_proxies, process_mock):
    subprocess_run_mock.return_value = process_mock
    proxy_setter = ProxySetter("windows")
    with pytest.raises(PipUrlException):
        proxy_setter.set(bad_proxies)
