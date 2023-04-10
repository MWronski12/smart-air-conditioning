from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddDeviceRequest(_message.Message):
    __slots__ = ["device", "room_id"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    device: Device
    room_id: str
    def __init__(self, room_id: _Optional[str] = ..., device: _Optional[_Union[Device, _Mapping]] = ...) -> None: ...

class AddDeviceResponse(_message.Message):
    __slots__ = ["device"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: Device
    def __init__(self, device: _Optional[_Union[Device, _Mapping]] = ...) -> None: ...

class AddRoomRequest(_message.Message):
    __slots__ = ["room"]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    room: Room
    def __init__(self, room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class AddRoomResponse(_message.Message):
    __slots__ = ["room"]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    room: Room
    def __init__(self, room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class AddUserRequest(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class AddUserResponse(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class AddUserToRoomRequest(_message.Message):
    __slots__ = ["room_id", "user_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., room_id: _Optional[str] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetAllRoomsResponse(_message.Message):
    __slots__ = ["rooms"]
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    rooms: _containers.RepeatedCompositeFieldContainer[Room]
    def __init__(self, rooms: _Optional[_Iterable[_Union[Room, _Mapping]]] = ...) -> None: ...

class GetDevicesInRoomRequest(_message.Message):
    __slots__ = ["room_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class GetDevicesInRoomResponse(_message.Message):
    __slots__ = ["devices"]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    def __init__(self, devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ...) -> None: ...

class GetRoomRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetRoomResponse(_message.Message):
    __slots__ = ["room"]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    room: Room
    def __init__(self, room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUsersInRoomRequest(_message.Message):
    __slots__ = ["room_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class GetUsersInRoomResponse(_message.Message):
    __slots__ = ["users"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class Preference(_message.Message):
    __slots__ = ["fan_speed", "temperature"]
    FAN_SPEED_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    fan_speed: int
    temperature: float
    def __init__(self, temperature: _Optional[float] = ..., fan_speed: _Optional[int] = ...) -> None: ...

class RemoveUserFromRoomRequest(_message.Message):
    __slots__ = ["room_id", "user_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., room_id: _Optional[str] = ...) -> None: ...

class Room(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class SetUserPreferencesRequest(_message.Message):
    __slots__ = ["preferences", "user_id"]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    preferences: Preference
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., preferences: _Optional[_Union[Preference, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["id", "name", "preferences"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    preferences: Preference
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., preferences: _Optional[_Union[Preference, _Mapping]] = ...) -> None: ...
