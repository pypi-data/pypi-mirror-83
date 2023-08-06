class PipException(Exception):
    pass


class PipNotInstalledException(PipException):
    pass


class PipInstallException(PipException):
    pass


class PipUnInstallException(PipException):
    pass


class PipRequestException(PipException):
    pass


class PipProxyException(PipException):
    pass


class PipUrlException(PipException):
    pass
