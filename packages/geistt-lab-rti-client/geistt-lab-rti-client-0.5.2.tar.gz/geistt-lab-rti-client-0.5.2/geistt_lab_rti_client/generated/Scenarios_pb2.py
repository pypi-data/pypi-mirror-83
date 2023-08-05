# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Scenarios.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Scenarios.proto',
  package='geistt.rti',
  syntax='proto3',
  serialized_options=b'\252\002\024GEISTT.Lab.RTI.Proto',
  serialized_pb=b'\n\x0fScenarios.proto\x12\ngeistt.rti\x1a\x1bgoogle/protobuf/empty.proto\"\xac\x01\n\tScenarios\x12\x33\n\x11request_scenarios\x18\x01 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12\x32\n\x08scenario\x18\x02 \x01(\x0b\x32\x1e.geistt.rti.Scenarios.ScenarioH\x00\x1a-\n\x08Scenario\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\tB\x07\n\x05whichB\x17\xaa\x02\x14GEISTT.Lab.RTI.Protob\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_SCENARIOS_SCENARIO = _descriptor.Descriptor(
  name='Scenario',
  full_name='geistt.rti.Scenarios.Scenario',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geistt.rti.Scenarios.Scenario.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='geistt.rti.Scenarios.Scenario.description', index=1,
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
  serialized_start=179,
  serialized_end=224,
)

_SCENARIOS = _descriptor.Descriptor(
  name='Scenarios',
  full_name='geistt.rti.Scenarios',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_scenarios', full_name='geistt.rti.Scenarios.request_scenarios', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scenario', full_name='geistt.rti.Scenarios.scenario', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SCENARIOS_SCENARIO, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='which', full_name='geistt.rti.Scenarios.which',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=61,
  serialized_end=233,
)

_SCENARIOS_SCENARIO.containing_type = _SCENARIOS
_SCENARIOS.fields_by_name['request_scenarios'].message_type = google_dot_protobuf_dot_empty__pb2._EMPTY
_SCENARIOS.fields_by_name['scenario'].message_type = _SCENARIOS_SCENARIO
_SCENARIOS.oneofs_by_name['which'].fields.append(
  _SCENARIOS.fields_by_name['request_scenarios'])
_SCENARIOS.fields_by_name['request_scenarios'].containing_oneof = _SCENARIOS.oneofs_by_name['which']
_SCENARIOS.oneofs_by_name['which'].fields.append(
  _SCENARIOS.fields_by_name['scenario'])
_SCENARIOS.fields_by_name['scenario'].containing_oneof = _SCENARIOS.oneofs_by_name['which']
DESCRIPTOR.message_types_by_name['Scenarios'] = _SCENARIOS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Scenarios = _reflection.GeneratedProtocolMessageType('Scenarios', (_message.Message,), {

  'Scenario' : _reflection.GeneratedProtocolMessageType('Scenario', (_message.Message,), {
    'DESCRIPTOR' : _SCENARIOS_SCENARIO,
    '__module__' : 'Scenarios_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Scenarios.Scenario)
    })
  ,
  'DESCRIPTOR' : _SCENARIOS,
  '__module__' : 'Scenarios_pb2'
  # @@protoc_insertion_point(class_scope:geistt.rti.Scenarios)
  })
_sym_db.RegisterMessage(Scenarios)
_sym_db.RegisterMessage(Scenarios.Scenario)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
