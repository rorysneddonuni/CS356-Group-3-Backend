from __future__ import annotations

from pydantic import BaseModel, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Info(BaseModel):
    """
    Info message for actions (i.e. create, delete)
    """  # noqa: E501
    message: StrictStr

    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
