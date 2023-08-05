"""
Main interface for iot-data service type definitions.

Usage::

    ```python
    from mypy_boto3_iot_data.type_defs import DeleteThingShadowResponseTypeDef

    data: DeleteThingShadowResponseTypeDef = {...}
    ```
"""
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "DeleteThingShadowResponseTypeDef",
    "GetThingShadowResponseTypeDef",
    "ListNamedShadowsForThingResponseTypeDef",
    "UpdateThingShadowResponseTypeDef",
)

DeleteThingShadowResponseTypeDef = TypedDict("DeleteThingShadowResponseTypeDef", {"payload": bytes})

GetThingShadowResponseTypeDef = TypedDict(
    "GetThingShadowResponseTypeDef", {"payload": bytes}, total=False
)

ListNamedShadowsForThingResponseTypeDef = TypedDict(
    "ListNamedShadowsForThingResponseTypeDef",
    {"results": List[str], "nextToken": str, "timestamp": int},
    total=False,
)

UpdateThingShadowResponseTypeDef = TypedDict(
    "UpdateThingShadowResponseTypeDef", {"payload": bytes}, total=False
)
