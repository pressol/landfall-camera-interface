# 📸 Landfall Camera Interface SDK

**The official Python SDK for building camera drivers for the Landfall Cinema Monitor.**

This SDK defines the contract (`CameraBackend`) that allows the **Landfall Monitor** to communicate with cinema cameras (RED, Sony, Arri, Canon, Blackmagic, etc.). By implementing this interface, you can add support for any camera to the Landfall ecosystem.

## 📦 Installation
pip install landfall-camera-interface

## 🚀 Quick Start: Building a Driver

To create a new driver, create a Python file (e.g., `my_custom_camera.py`) and subclass `CameraBackend`.

```python
import asyncio
from landfall_interface.interface import CameraBackend, CameraState
from typing import Any

class MyCustomCamera(CameraBackend):
    def __init__(self):
        super().__init__()
        # Initialize your camera SDK or connection libraries here
      
    async def connect(self, identifier: str) -> bool:
        print(f"Connecting to {identifier}...")
          
        # Simulate connection success
        self.connection_status.emit(True, "Connected")
          
        # Update initial state
        self.state.iso = "800"
        self.state.shutter = "180"
        self.state_changed.emit(self.state)
        return True
  
    async def start_record(self):
        print("Triggering Record...")
        self.state.recording = True
        self.state_changed.emit(self.state)
  
    async def stop_record(self):
        print("Stopping Record...")
        self.state.recording = False
        self.state_changed.emit(self.state)
  
    async def set_parameter(self, param: str, value: Any):
        if param == "iso":
            self.state.iso = str(value)
        self.state_changed.emit(self.state)
  
    async def disconnect(self):
        self.connection_status.emit(False, "Disconnected")
  
    async def inject_metadata(self, metadata: dict):
        # Handle slate data injection (Scene, Take, etc.)
        pass
```
## 🔌 How to Load Your Driver
The Landfall Monitor supports "side-loading" drivers without recompiling the main application.
Write your driver script (as shown above).
Copy your .py file to the Landfall plugins directory on the device:
Linux: ~/.landfall/drivers/
Restart the Landfall Monitor. Your driver will be automatically discovered and loaded.
## 📚 API Reference
CameraState (Dataclass)
Holds the current status of the camera.
Parameter	Type	Description
recording	bool	Is the camera rolling?
iso	str	Current ISO/Gain.
shutter	str	Current Shutter Angle or Speed.
iris	str	Aperture value.
white_balance	str	Kelvin value.
battery_voltage	float	Input voltage.
CameraBackend (Abstract Base Class)
Your driver must inherit from this and implement the following async methods:
Method	Signature	Description
connect	connect(identifier: str)	Initialize connection (BLE MAC, IP, or Serial Port).
disconnect	disconnect()	Clean up resources.
start_record	start_record()	Trigger recording.
stop_record	stop_record()	End recording.
set_parameter	set_parameter(param, value)	Update camera settings.
inject_metadata	inject_metadata(metadata)	Send slate/logging info to the camera.
Signals (PySide6)
Signal	Arguments	Description
state_changed	(CameraState)	Emit this whenever a setting changes on the camera so the UI updates.
connection_status	(bool, str)	Emit (True, "Message") on connect or (False, "Error") on failure.
## 🤝 Contributing
We welcome community drivers! If you have reverse-engineered a protocol for a new camera:
Fork this repository.
Create your driver in the examples folder.
Submit a Pull Request.
## 📄 License
This SDK is open-source under the MIT License.
 