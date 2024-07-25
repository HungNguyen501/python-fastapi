from typing import Any, Dict
from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(404, detail, headers)