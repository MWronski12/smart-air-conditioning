from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Settings(_message.Message):
    __slots__ = ["device_id", "fan_speed", "room_id", "temperature"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FAN_SPEED_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    fan_speed: int
    room_id: str
    temperature: float
    def __init__(self, room_id: _Optional[str] = ..., device_id: _Optional[str] = ..., temperature: _Optional[float] = ..., fan_speed: _Optional[int] = ...) -> None: ...
