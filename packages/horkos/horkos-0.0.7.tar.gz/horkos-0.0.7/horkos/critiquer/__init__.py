from horkos.critiquer import _casing
from horkos.critiquer import _typing


_GLOBAL_CRITIQUERS = [
    _casing.global_prefer_snake_case,
    _casing.global_field_casing_check,
    _typing.global_type_consistency_check,
]
_RELATIVE_CRITIQUERS = [
    _casing.relative_field_casing_check,
    _typing.relative_type_consistency_check,
]
_LOCAL_CRITIQUERS = [
    _casing.local_prefer_snake_case,
    _casing.local_uniform_field_casing_check,
]
