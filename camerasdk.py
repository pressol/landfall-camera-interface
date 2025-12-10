from abc import ABC, abstractmethod, ABCMeta
from PySide6.QtCore import QObject, Signal
from dataclasses import dataclass
from typing import Any, Dict


# Metaclass to resolve conflict between QObject (C++) and ABC (Python)
class QABCMeta(type(QObject), ABCMeta):
    pass


@dataclass
class CameraState:
    recording: bool = False
    iso: str = "N/A"
    shutter: str = "N/A"
    iris: str = "N/A"
    white_balance: str = "N/A"
    battery_voltage: float = 0.0
    lens_info: str = ""


class CameraBackend(QObject, ABC, metaclass=QABCMeta):
    """
    The Public API for Landfall Camera Drivers.
    Community drivers must inherit from this class.
    """
    # PySide6 Signals
    state_changed = Signal(object)  # Emits CameraState
    connection_status = Signal(bool, str)  # (Connected?, Message)

    def __init__(self):
        super().__init__()
        self.state = CameraState()

    @abstractmethod
    async def connect(self, identifier: str) -> bool:
        """
        Connect to camera.
        identifier: IP address, Bluetooth MAC, or Serial Port.
        """
        pass

    @abstractmethod
    async def disconnect(self):
        """Clean resource cleanup."""
        pass

    @abstractmethod
    async def start_record(self):
        pass

    @abstractmethod
    async def stop_record(self):
        pass

    @abstractmethod
    async def set_parameter(self, param: str, value: Any):
        """
        Generic setter.
        param: 'iso', 'shutter', 'iris', 'wb'
        """
        pass

    @abstractmethod
    async def inject_metadata(self, metadata: Dict[str, Any]):
        """
        Inject slate data (Scene, Take, Prod Name) into camera.
        """
        pass