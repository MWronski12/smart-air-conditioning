from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PublishDeviceSettingsRequest(_message.Message):
    __slots__ = ["settings"]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    settings: Settings
    def __init__(self, settings: _Optional[_Union[Settings, _Mapping]] = ...) -> None: ...

class PublishDeviceSettingsResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

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
