# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: record.proto

import sys

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="record.proto",
    package="aialgs.data",
    syntax="proto2",
    serialized_pb=_b(
        '\n\x0crecord.proto\x12\x0b\x61ialgs.data"H\n\rFloat32Tensor\x12\x12\n\x06values\x18\x01 \x03(\x02\x42\x02\x10\x01\x12\x10\n\x04keys\x18\x02 \x03(\x04\x42\x02\x10\x01\x12\x11\n\x05shape\x18\x03 \x03(\x04\x42\x02\x10\x01"H\n\rFloat64Tensor\x12\x12\n\x06values\x18\x01 \x03(\x01\x42\x02\x10\x01\x12\x10\n\x04keys\x18\x02 \x03(\x04\x42\x02\x10\x01\x12\x11\n\x05shape\x18\x03 \x03(\x04\x42\x02\x10\x01"F\n\x0bInt32Tensor\x12\x12\n\x06values\x18\x01 \x03(\x05\x42\x02\x10\x01\x12\x10\n\x04keys\x18\x02 \x03(\x04\x42\x02\x10\x01\x12\x11\n\x05shape\x18\x03 \x03(\x04\x42\x02\x10\x01",\n\x05\x42ytes\x12\r\n\x05value\x18\x01 \x03(\x0c\x12\x14\n\x0c\x63ontent_type\x18\x02 \x01(\t"\xd3\x01\n\x05Value\x12\x34\n\x0e\x66loat32_tensor\x18\x02 \x01(\x0b\x32\x1a.aialgs.data.Float32TensorH\x00\x12\x34\n\x0e\x66loat64_tensor\x18\x03 \x01(\x0b\x32\x1a.aialgs.data.Float64TensorH\x00\x12\x30\n\x0cint32_tensor\x18\x07 \x01(\x0b\x32\x18.aialgs.data.Int32TensorH\x00\x12#\n\x05\x62ytes\x18\t \x01(\x0b\x32\x12.aialgs.data.BytesH\x00\x42\x07\n\x05value"\xa9\x02\n\x06Record\x12\x33\n\x08\x66\x65\x61tures\x18\x01 \x03(\x0b\x32!.aialgs.data.Record.FeaturesEntry\x12-\n\x05label\x18\x02 \x03(\x0b\x32\x1e.aialgs.data.Record.LabelEntry\x12\x0b\n\x03uid\x18\x03 \x01(\t\x12\x10\n\x08metadata\x18\x04 \x01(\t\x12\x15\n\rconfiguration\x18\x05 \x01(\t\x1a\x43\n\rFeaturesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.aialgs.data.Value:\x02\x38\x01\x1a@\n\nLabelEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.aialgs.data.Value:\x02\x38\x01\x42\x30\n com.amazonaws.aialgorithms.protoB\x0cRecordProtos'
    ),
)


_FLOAT32TENSOR = _descriptor.Descriptor(
    name="Float32Tensor",
    full_name="aialgs.data.Float32Tensor",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="values",
            full_name="aialgs.data.Float32Tensor.values",
            index=0,
            number=1,
            type=2,
            cpp_type=6,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="keys",
            full_name="aialgs.data.Float32Tensor.keys",
            index=1,
            number=2,
            type=4,
            cpp_type=4,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="shape",
            full_name="aialgs.data.Float32Tensor.shape",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=29,
    serialized_end=101,
)


_FLOAT64TENSOR = _descriptor.Descriptor(
    name="Float64Tensor",
    full_name="aialgs.data.Float64Tensor",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="values",
            full_name="aialgs.data.Float64Tensor.values",
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="keys",
            full_name="aialgs.data.Float64Tensor.keys",
            index=1,
            number=2,
            type=4,
            cpp_type=4,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="shape",
            full_name="aialgs.data.Float64Tensor.shape",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=103,
    serialized_end=175,
)


_INT32TENSOR = _descriptor.Descriptor(
    name="Int32Tensor",
    full_name="aialgs.data.Int32Tensor",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="values",
            full_name="aialgs.data.Int32Tensor.values",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="keys",
            full_name="aialgs.data.Int32Tensor.keys",
            index=1,
            number=2,
            type=4,
            cpp_type=4,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="shape",
            full_name="aialgs.data.Int32Tensor.shape",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=177,
    serialized_end=247,
)


_BYTES = _descriptor.Descriptor(
    name="Bytes",
    full_name="aialgs.data.Bytes",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="value",
            full_name="aialgs.data.Bytes.value",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="content_type",
            full_name="aialgs.data.Bytes.content_type",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=249,
    serialized_end=293,
)


_VALUE = _descriptor.Descriptor(
    name="Value",
    full_name="aialgs.data.Value",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="float32_tensor",
            full_name="aialgs.data.Value.float32_tensor",
            index=0,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="float64_tensor",
            full_name="aialgs.data.Value.float64_tensor",
            index=1,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="int32_tensor",
            full_name="aialgs.data.Value.int32_tensor",
            index=2,
            number=7,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="bytes",
            full_name="aialgs.data.Value.bytes",
            index=3,
            number=9,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="value",
            full_name="aialgs.data.Value.value",
            index=0,
            containing_type=None,
            fields=[],
        )
    ],
    serialized_start=296,
    serialized_end=507,
)


_RECORD_FEATURESENTRY = _descriptor.Descriptor(
    name="FeaturesEntry",
    full_name="aialgs.data.Record.FeaturesEntry",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="key",
            full_name="aialgs.data.Record.FeaturesEntry.key",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="aialgs.data.Record.FeaturesEntry.value",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b("8\001")),
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=674,
    serialized_end=741,
)

_RECORD_LABELENTRY = _descriptor.Descriptor(
    name="LabelEntry",
    full_name="aialgs.data.Record.LabelEntry",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="key",
            full_name="aialgs.data.Record.LabelEntry.key",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="aialgs.data.Record.LabelEntry.value",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b("8\001")),
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=743,
    serialized_end=807,
)

_RECORD = _descriptor.Descriptor(
    name="Record",
    full_name="aialgs.data.Record",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="features",
            full_name="aialgs.data.Record.features",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="label",
            full_name="aialgs.data.Record.label",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="uid",
            full_name="aialgs.data.Record.uid",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="metadata",
            full_name="aialgs.data.Record.metadata",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="configuration",
            full_name="aialgs.data.Record.configuration",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[_RECORD_FEATURESENTRY, _RECORD_LABELENTRY],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=510,
    serialized_end=807,
)

_VALUE.fields_by_name["float32_tensor"].message_type = _FLOAT32TENSOR
_VALUE.fields_by_name["float64_tensor"].message_type = _FLOAT64TENSOR
_VALUE.fields_by_name["int32_tensor"].message_type = _INT32TENSOR
_VALUE.fields_by_name["bytes"].message_type = _BYTES
_VALUE.oneofs_by_name["value"].fields.append(_VALUE.fields_by_name["float32_tensor"])
_VALUE.fields_by_name["float32_tensor"].containing_oneof = _VALUE.oneofs_by_name["value"]
_VALUE.oneofs_by_name["value"].fields.append(_VALUE.fields_by_name["float64_tensor"])
_VALUE.fields_by_name["float64_tensor"].containing_oneof = _VALUE.oneofs_by_name["value"]
_VALUE.oneofs_by_name["value"].fields.append(_VALUE.fields_by_name["int32_tensor"])
_VALUE.fields_by_name["int32_tensor"].containing_oneof = _VALUE.oneofs_by_name["value"]
_VALUE.oneofs_by_name["value"].fields.append(_VALUE.fields_by_name["bytes"])
_VALUE.fields_by_name["bytes"].containing_oneof = _VALUE.oneofs_by_name["value"]
_RECORD_FEATURESENTRY.fields_by_name["value"].message_type = _VALUE
_RECORD_FEATURESENTRY.containing_type = _RECORD
_RECORD_LABELENTRY.fields_by_name["value"].message_type = _VALUE
_RECORD_LABELENTRY.containing_type = _RECORD
_RECORD.fields_by_name["features"].message_type = _RECORD_FEATURESENTRY
_RECORD.fields_by_name["label"].message_type = _RECORD_LABELENTRY
DESCRIPTOR.message_types_by_name["Float32Tensor"] = _FLOAT32TENSOR
DESCRIPTOR.message_types_by_name["Float64Tensor"] = _FLOAT64TENSOR
DESCRIPTOR.message_types_by_name["Int32Tensor"] = _INT32TENSOR
DESCRIPTOR.message_types_by_name["Bytes"] = _BYTES
DESCRIPTOR.message_types_by_name["Value"] = _VALUE
DESCRIPTOR.message_types_by_name["Record"] = _RECORD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Float32Tensor = _reflection.GeneratedProtocolMessageType(
    "Float32Tensor",
    (_message.Message,),
    dict(
        DESCRIPTOR=_FLOAT32TENSOR,
        __module__="record_pb2"
        # @@protoc_insertion_point(class_scope:aialgs.data.Float32Tensor)
    ),
)
_sym_db.RegisterMessage(Float32Tensor)

Float64Tensor = _reflection.GeneratedProtocolMessageType(
    "Float64Tensor",
    (_message.Message,),
    dict(
        DESCRIPTOR=_FLOAT64TENSOR,
        __module__="record_pb2"
        # @@protoc_insertion_point(class_scope:aialgs.data.Float64Tensor)
    ),
)
_sym_db.RegisterMessage(Float64Tensor)

Int32Tensor = _reflection.GeneratedProtocolMessageType(
    "Int32Tensor",
    (_message.Message,),
    dict(
        DESCRIPTOR=_INT32TENSOR,
        __module__="record_pb2"
        # @@protoc_insertion_point(class_scope:aialgs.data.Int32Tensor)
    ),
)
_sym_db.RegisterMessage(Int32Tensor)

Bytes = _reflection.GeneratedProtocolMessageType(
    "Bytes",
    (_message.Message,),
    dict(
        DESCRIPTOR=_BYTES,
        __module__="record_pb2"
        # @@protoc_insertion_point(class_scope:aialgs.data.Bytes)
    ),
)
_sym_db.RegisterMessage(Bytes)

Value = _reflection.GeneratedProtocolMessageType(
    "Value",
    (_message.Message,),
    dict(
        DESCRIPTOR=_VALUE,
        __module__="record_pb2"
        # @@protoc_insertion_point(class_scope:aialgs.data.Value)
    ),
)
_sym_db.RegisterMessage(Value)

Record = _reflection.GeneratedProtocolMessageType(
    "Record",
    (_message.Message,),
    dict(
        FeaturesEntry=_reflection.GeneratedProtocolMessageType(
            "FeaturesEntry",
            (_message.Message,),
            dict(
                DESCRIPTOR=_RECORD_FEATURESENTRY,
                __module__="record_pb2"
                # @@protoc_insertion_point(class_scope:aialgs.data.Record.FeaturesEntry)
            ),
        ),
        LabelEntry=_reflection.GeneratedProtocolMessageType(
            "LabelEntry",
            (_message.Message,),
            dict(
                DESCRIPTOR=_RECORD_LABELENTRY,
                __module__="record_pb2"
                # @@protoc_insertion_point(class_scope:aialgs.data.Record.LabelEntry)
            ),
        ),
        DESCRIPTOR=_RECORD,
        __module__="record_pb2"
        # @@protoc_insertion_point(class_scope:aialgs.data.Record)
    ),
)
_sym_db.RegisterMessage(Record)
_sym_db.RegisterMessage(Record.FeaturesEntry)
_sym_db.RegisterMessage(Record.LabelEntry)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(
    descriptor_pb2.FileOptions(), _b("\n com.amazonaws.aialgorithms.protoB\014RecordProtos")
)
_FLOAT32TENSOR.fields_by_name["values"].has_options = True
_FLOAT32TENSOR.fields_by_name["values"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_FLOAT32TENSOR.fields_by_name["keys"].has_options = True
_FLOAT32TENSOR.fields_by_name["keys"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_FLOAT32TENSOR.fields_by_name["shape"].has_options = True
_FLOAT32TENSOR.fields_by_name["shape"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_FLOAT64TENSOR.fields_by_name["values"].has_options = True
_FLOAT64TENSOR.fields_by_name["values"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_FLOAT64TENSOR.fields_by_name["keys"].has_options = True
_FLOAT64TENSOR.fields_by_name["keys"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_FLOAT64TENSOR.fields_by_name["shape"].has_options = True
_FLOAT64TENSOR.fields_by_name["shape"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_INT32TENSOR.fields_by_name["values"].has_options = True
_INT32TENSOR.fields_by_name["values"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_INT32TENSOR.fields_by_name["keys"].has_options = True
_INT32TENSOR.fields_by_name["keys"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_INT32TENSOR.fields_by_name["shape"].has_options = True
_INT32TENSOR.fields_by_name["shape"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_RECORD_FEATURESENTRY.has_options = True
_RECORD_FEATURESENTRY._options = _descriptor._ParseOptions(
    descriptor_pb2.MessageOptions(), _b("8\001")
)
_RECORD_LABELENTRY.has_options = True
_RECORD_LABELENTRY._options = _descriptor._ParseOptions(
    descriptor_pb2.MessageOptions(), _b("8\001")
)
# @@protoc_insertion_point(module_scope)
