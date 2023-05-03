from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Measurement(_message.Message):
    __slots__ = ["device_id", "humidity", "room_id", "temperature"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    humidity: float
    room_id: str
    temperature: float
    def __init__(self, room_id: _Optional[str] = ..., device_id: _Optional[str] = ..., temperature: _Optional[float] = ..., humidity: _Optional[float] = ...) -> None: ...

class ReadMeasurementsRequest(_message.Message):
    __slots__ = ["device_id", "end_time", "has_humidity", "has_temperature", "room_id", "start_time"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    HAS_HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    HAS_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    end_time: int
    has_humidity: bool
    has_temperature: bool
    room_id: str
    start_time: int
    def __init__(self, room_id: _Optional[str] = ..., device_id: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., has_temperature: bool = ..., has_humidity: bool = ...) -> None: ...

class ReadMeasurementsResponse(_message.Message):
    __slots__ = ["measurement"]
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    measurement: _containers.RepeatedCompositeFieldContainer[Measurement]
    def __init__(self, measurement: _Optional[_Iterable[_Union[Measurement, _Mapping]]] = ...) -> None: ...

class WriteMeasurementRequest(_message.Message):
    __slots__ = ["measurement"]
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    measurement: Measurement
    def __init__(self, measurement: _Optional[_Union[Measurement, _Mapping]] = ...) -> None: ...

class WriteMeasurementResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
