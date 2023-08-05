# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Channels.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Channels.proto',
  package='geistt.rti',
  syntax='proto3',
  serialized_options=b'\252\002\024GEISTT.Lab.RTI.Proto',
  serialized_pb=b'\n\x0e\x43hannels.proto\x12\ngeistt.rti\x1a\x1bgoogle/protobuf/empty.proto\"\x9b\x03\n\x08\x43hannels\x12\x37\n\x15request_channel_usage\x18\x01 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12:\n\rchannel_usage\x18\x02 \x01(\x0b\x32!.geistt.rti.Channels.ChannelUsageH\x00\x12/\n\x07\x63hannel\x18\x03 \x01(\x0b\x32\x1c.geistt.rti.Channels.ChannelH\x00\x1aS\n\x0c\x43hannelUsage\x12\x13\n\x0binstance_id\x18\x01 \x01(\t\x12.\n\x05usage\x18\x02 \x03(\x0b\x32\x1f.geistt.rti.Channels.ChannelUse\x1a_\n\nChannelUse\x12-\n\x07\x63hannel\x18\x01 \x01(\x0b\x32\x1c.geistt.rti.Channels.Channel\x12\x0f\n\x07publish\x18\x03 \x01(\x08\x12\x11\n\tsubscribe\x18\x04 \x01(\x08\x1a*\n\x07\x43hannel\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tdata_type\x18\x02 \x01(\tB\x07\n\x05whichB\x17\xaa\x02\x14GEISTT.Lab.RTI.Protob\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_CHANNELS_CHANNELUSAGE = _descriptor.Descriptor(
  name='ChannelUsage',
  full_name='geistt.rti.Channels.ChannelUsage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance_id', full_name='geistt.rti.Channels.ChannelUsage.instance_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='usage', full_name='geistt.rti.Channels.ChannelUsage.usage', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=238,
  serialized_end=321,
)

_CHANNELS_CHANNELUSE = _descriptor.Descriptor(
  name='ChannelUse',
  full_name='geistt.rti.Channels.ChannelUse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='channel', full_name='geistt.rti.Channels.ChannelUse.channel', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='publish', full_name='geistt.rti.Channels.ChannelUse.publish', index=1,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='subscribe', full_name='geistt.rti.Channels.ChannelUse.subscribe', index=2,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=323,
  serialized_end=418,
)

_CHANNELS_CHANNEL = _descriptor.Descriptor(
  name='Channel',
  full_name='geistt.rti.Channels.Channel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geistt.rti.Channels.Channel.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data_type', full_name='geistt.rti.Channels.Channel.data_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=420,
  serialized_end=462,
)

_CHANNELS = _descriptor.Descriptor(
  name='Channels',
  full_name='geistt.rti.Channels',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_channel_usage', full_name='geistt.rti.Channels.request_channel_usage', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='channel_usage', full_name='geistt.rti.Channels.channel_usage', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='channel', full_name='geistt.rti.Channels.channel', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CHANNELS_CHANNELUSAGE, _CHANNELS_CHANNELUSE, _CHANNELS_CHANNEL, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='which', full_name='geistt.rti.Channels.which',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=60,
  serialized_end=471,
)

_CHANNELS_CHANNELUSAGE.fields_by_name['usage'].message_type = _CHANNELS_CHANNELUSE
_CHANNELS_CHANNELUSAGE.containing_type = _CHANNELS
_CHANNELS_CHANNELUSE.fields_by_name['channel'].message_type = _CHANNELS_CHANNEL
_CHANNELS_CHANNELUSE.containing_type = _CHANNELS
_CHANNELS_CHANNEL.containing_type = _CHANNELS
_CHANNELS.fields_by_name['request_channel_usage'].message_type = google_dot_protobuf_dot_empty__pb2._EMPTY
_CHANNELS.fields_by_name['channel_usage'].message_type = _CHANNELS_CHANNELUSAGE
_CHANNELS.fields_by_name['channel'].message_type = _CHANNELS_CHANNEL
_CHANNELS.oneofs_by_name['which'].fields.append(
  _CHANNELS.fields_by_name['request_channel_usage'])
_CHANNELS.fields_by_name['request_channel_usage'].containing_oneof = _CHANNELS.oneofs_by_name['which']
_CHANNELS.oneofs_by_name['which'].fields.append(
  _CHANNELS.fields_by_name['channel_usage'])
_CHANNELS.fields_by_name['channel_usage'].containing_oneof = _CHANNELS.oneofs_by_name['which']
_CHANNELS.oneofs_by_name['which'].fields.append(
  _CHANNELS.fields_by_name['channel'])
_CHANNELS.fields_by_name['channel'].containing_oneof = _CHANNELS.oneofs_by_name['which']
DESCRIPTOR.message_types_by_name['Channels'] = _CHANNELS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Channels = _reflection.GeneratedProtocolMessageType('Channels', (_message.Message,), {

  'ChannelUsage' : _reflection.GeneratedProtocolMessageType('ChannelUsage', (_message.Message,), {
    'DESCRIPTOR' : _CHANNELS_CHANNELUSAGE,
    '__module__' : 'Channels_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Channels.ChannelUsage)
    })
  ,

  'ChannelUse' : _reflection.GeneratedProtocolMessageType('ChannelUse', (_message.Message,), {
    'DESCRIPTOR' : _CHANNELS_CHANNELUSE,
    '__module__' : 'Channels_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Channels.ChannelUse)
    })
  ,

  'Channel' : _reflection.GeneratedProtocolMessageType('Channel', (_message.Message,), {
    'DESCRIPTOR' : _CHANNELS_CHANNEL,
    '__module__' : 'Channels_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Channels.Channel)
    })
  ,
  'DESCRIPTOR' : _CHANNELS,
  '__module__' : 'Channels_pb2'
  # @@protoc_insertion_point(class_scope:geistt.rti.Channels)
  })
_sym_db.RegisterMessage(Channels)
_sym_db.RegisterMessage(Channels.ChannelUsage)
_sym_db.RegisterMessage(Channels.ChannelUse)
_sym_db.RegisterMessage(Channels.Channel)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
