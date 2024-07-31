"""
Models for generated SQL
"""
from typing import List, Optional

from pydantic.class_validators import root_validator
from pydantic.main import BaseModel

from datajunction_server.models.engine import Dialect
from datajunction_server.models.query import ColumnMetadata
from datajunction_server.transpilation import get_transpilation_plugin
from datajunction_server.utils import get_settings


class NodeNameVersion(BaseModel):
    """
    Node name and version
    """

    name: str
    version: str

    class Config:  # pylint: disable=missing-class-docstring,too-few-public-methods
        orm_mode = True


class GeneratedSQL(BaseModel):
    """
    Generated SQL for a given node, the output of a QueryBuilder(...).build() call.
    """

    node: NodeNameVersion
    sql: str
    columns: Optional[List[ColumnMetadata]] = None  # pragma: no-cover
    dialect: Optional[Dialect] = None
    upstream_tables: Optional[List[str]] = None

    @root_validator(pre=False)
    def transpile_sql(  # pylint: disable=no-self-argument
        cls,
        values,
    ):
        """
        Transpiles SQL to the specified dialect with the configured transpilation plugin.
        If no plugin is configured, it will just return the original generated query.
        """
        settings = get_settings()
        if settings.sql_transpilation_library:
            plugin = get_transpilation_plugin(settings.sql_transpilation_library)
            values["sql"] = plugin.transpile_sql(
                values["sql"],
                input_dialect=Dialect.SPARK,
                output_dialect=values["dialect"],
            )
        return values
