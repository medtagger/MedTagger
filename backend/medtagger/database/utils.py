"""Utils methods for database module."""
import re
from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

from medtagger.api.exceptions import InternalErrorException


class ArrayOfEnum(ARRAY):  # pylint: disable=too-many-ancestors
    """Helper class for processing enums arrays."""

    def bind_expression(self, bindvalue: Any) -> Any:
        """Given a bind value (i.e. a BindParameter instance), return a SQL expression in its place."""
        return sa.cast(bindvalue, self)

    def result_processor(self, dialect: Any, coltype: Any) -> Any:
        """Return a conversion function for processing result row values."""
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value: Any) -> Any:
            """Parse raw string values of Enum and return list of values."""
            inner = re.match(r"^{(.*)}$", value)
            if not inner:
                raise InternalErrorException('Enum values did not match the pattern!')
            return inner.group(1).split(",")

        def process(value: Any) -> Any:
            """Process raw SQL value."""
            return super_rp(handle_raw_string(value))

        return process
