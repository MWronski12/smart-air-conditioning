# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/protos/logic.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x61pp/protos/logic.proto\x12\x05logic\"4\n!NotifyUserPreferenceChangeRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"5\n\"NotifyUserPreferenceChangeResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"?\n\x1bNotifyUserRoomChangeRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07room_id\x18\x02 \x01(\t\"@\n\x1cNotifyUserRoomChangeResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07room_id\x18\x02 \x01(\t2\xe6\x01\n\x0cLogicService\x12s\n\x1aNotifyUserPreferenceChange\x12(.logic.NotifyUserPreferenceChangeRequest\x1a).logic.NotifyUserPreferenceChangeResponse\"\x00\x12\x61\n\x14NotifyUserRoomChange\x12\".logic.NotifyUserRoomChangeRequest\x1a#.logic.NotifyUserRoomChangeResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'app.protos.logic_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NOTIFYUSERPREFERENCECHANGEREQUEST._serialized_start=33
  _NOTIFYUSERPREFERENCECHANGEREQUEST._serialized_end=85
  _NOTIFYUSERPREFERENCECHANGERESPONSE._serialized_start=87
  _NOTIFYUSERPREFERENCECHANGERESPONSE._serialized_end=140
  _NOTIFYUSERROOMCHANGEREQUEST._serialized_start=142
  _NOTIFYUSERROOMCHANGEREQUEST._serialized_end=205
  _NOTIFYUSERROOMCHANGERESPONSE._serialized_start=207
  _NOTIFYUSERROOMCHANGERESPONSE._serialized_end=271
  _LOGICSERVICE._serialized_start=274
  _LOGICSERVICE._serialized_end=504
# @@protoc_insertion_point(module_scope)
