from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NotifyUserPreferenceChangeRequest(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class NotifyUserPreferenceChangeResponse(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class NotifyUserRoomChangeRequest(_message.Message):
    __slots__ = ["room_id", "user_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., room_id: _Optional[str] = ...) -> None: ...

class NotifyUserRoomChangeResponse(_message.Message):
    __slots__ = ["room_id", "user_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., room_id: _Optional[str] = ...) -> None: ...
