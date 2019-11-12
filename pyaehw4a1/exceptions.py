class AehW4a1Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ConnectionError(AehW4a1Error):
    """Exception raised for errors in connection."""
    def __init__(self, message):
        self.message = message

class HostError(AehW4a1Error):
    """Raised when host is invalid or missing."""
    def __init__(self, message):
        self.message = message
        
class UnkCmdError(AehW4a1Error):
    """Raised when command is not implemented."""
    def __init__(self, message):
        self.message = message
        
class UnkPacketError(AehW4a1Error):
    """Raised when packet is unknown."""
    def __init__(self, message):
        self.message = message
        
class UnkDataError(AehW4a1Error):
    """Raised when data is unknown."""
    def __init__(self, message):
        self.message = message
        
class WrongRespError(AehW4a1Error):
    """Raised when response is wrong."""
    def __init__(self, message):
        self.message = message
        
class WrongArgError(AehW4a1Error):
    """Raised when argument is wrong."""
    def __init__(self, message):
        self.message = message
        
class NoNetworksError(AehW4a1Error):
    """Raised when no network interfaces."""
    def __init__(self, message):
        self.message = message