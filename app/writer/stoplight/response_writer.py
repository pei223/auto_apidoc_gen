from collections import OrderedDict
from typing import Dict, Optional

from ...domain.value_objects.parameters import (
    SchemaParamInfo,
    ValueSchemaParam,
    FirstObjectSchemaParam,
    ObjectSchemaParam,
    ArraySchemaParam,
    RefSchemaParam,
)


def convert_openapi_schema(
        param_info: SchemaParamInfo, prev_param_info: Optional[SchemaParamInfo] = None
) -> Dict[str, any] or str:
    if isinstance(param_info, ObjectSchemaParam) or isinstance(param_info, FirstObjectSchemaParam):
        properties = OrderedDict()
        for prop in param_info.properties:
            properties.update(convert_openapi_schema(prop, param_info))
        row = OrderedDict({"type": "object", "properties": properties})
        return (
            row if isinstance(prev_param_info, ArraySchemaParam) or prev_param_info is None else {param_info.name: row}
        )
    if isinstance(param_info, ArraySchemaParam):
        return {
            param_info.name: OrderedDict(
                {"type": "array", "items": convert_openapi_schema(param_info.items, param_info)}
            )
        }

    if isinstance(param_info, RefSchemaParam):
        row = OrderedDict({"$ref": param_info.ref_path})
        return row if isinstance(prev_param_info, ArraySchemaParam) or not prev_param_info else {param_info.name: row}

    if isinstance(param_info, ValueSchemaParam):
        row = OrderedDict({"type": param_info.type.value})
        return row if isinstance(prev_param_info, ArraySchemaParam) else {param_info.name: row}
