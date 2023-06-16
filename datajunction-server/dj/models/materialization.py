"""Models for materialization"""
import enum
import zlib
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseModel
from sqlalchemy import JSON
from sqlalchemy import Column as SqlaColumn
from sqlalchemy import String
from sqlmodel import Field, Relationship, SQLModel

from dj.models.base import BaseSQLModel
from dj.models.engine import Engine, EngineInfo, EngineRef

if TYPE_CHECKING:
    from dj.models import NodeRevision


class GenericMaterializationInput(BaseModel):
    """
    The input when calling the query service's materialization
    API endpoint for a generic node.
    """

    name: str
    node_name: str
    node_type: str
    schedule: str
    query: str
    upstream_tables: List[str]
    spark_conf: Optional[Dict] = None
    partitions: Optional[List[Dict]] = None


class DruidMaterializationInput(GenericMaterializationInput):
    """
    The input when calling the query service's materialization
    API endpoint for a cube node.
    """

    druid_spec: Dict


class MaterializationInfo(BaseModel):
    """
    The output when calling the query service's materialization
    API endpoint for a cube node.
    """

    output_tables: List[str]
    urls: List[AnyHttpUrl]


class MaterializationConfigOutput(SQLModel):
    """
    Output for materialization config.
    """

    name: Optional[str]
    engine: EngineInfo
    config: Dict
    schedule: str
    job: str


class MaterializationConfigInfoUnified(
    MaterializationInfo,
    MaterializationConfigOutput,
):
    """
    Materialization config + info
    """


class UpsertMaterializationConfig(BaseSQLModel):
    """
    An upsert object for materialization configs
    """

    name: Optional[str]
    engine: EngineRef
    config: Dict
    schedule: str


class SparkConf(BaseSQLModel):
    """Spark configuration"""

    __root__: Dict[str, str]


class PartitionType(str, enum.Enum):
    """
    Partition type.

    A partition can be temporal or categorical
    """

    TEMPORAL = "temporal"
    CATEGORICAL = "categorical"


class Partition(BaseSQLModel):
    """
    A partition specification tells the ongoing and backfill materialization jobs how to partition
    the materialized dataset and which partition values (a list or range of values) to operate on.
    Partitions may be temporal or categorical and will be handled differently depending on the type.

    For temporal partition types, the ongoing materialization job will continue to operate on the
    latest partitions and the partition values specified by `values` and `range` are only relevant
    to the backfill job.

    Examples:
        This will tell DJ to backfill for all values of the dateint partition:
          Partition(name=“dateint”, type="temporal", values=[], range=())
        This will tell DJ to backfill just 20230601 and 20230605:
          Partition(name=“dateint”, type="temporal", values=[20230601, 20230605], range=())
        This will tell DJ to backfill 20230601 and between 20220101 and 20230101:
          Partition(name=“dateint”, type="temporal", values=[20230601], range=(20220101, 20230101))

        For categorical partition types, the ongoing materialization job will *only* operate on the
        specified partition values in `values` and `range`:
            Partition(name=“group_id”, type="categorical", values=["a", "b", "c"], range=())
    """

    name: str
    values: Optional[List]
    range: Optional[List]

    # This expression evaluates to the temporal partition value for scheduled runs
    expression: Optional[str]

    type_: PartitionType


class GenericMaterializationConfig(BaseModel):
    """
    Generic node materialization config needed by any materialization choices
    and engine combinations
    """

    query: Optional[str]

    # List of partitions that materialization jobs (ongoing and backfill) will operate on.
    partitions: Optional[List[Partition]]

    spark: Optional[SparkConf]
    upstream_tables: Optional[List[str]]

    def identifier(self) -> str:
        """
        Generates an identifier for this materialization config that is used by default
        for the materialization config's name if one is not set. Note that this name is
        based on partition names (both temporal and categorical) and partition values
        (only categorical).
        """
        entities = ["default"] if not self.partitions else []
        partitions_values = ""
        if self.partitions:
            for partition in self.partitions:
                if partition.type_ != PartitionType.TEMPORAL:
                    if partition.values:
                        partitions_values += str(partition.values)
                    if partition.range is not None:  # pragma: no cover
                        partitions_values += str(partition.range)
                entities.append(partition.name)
            entities.append(str(zlib.crc32(partitions_values.encode("utf-8"))))
        return "_".join(entities)


class Materialization(BaseSQLModel, table=True):  # type: ignore
    """
    Materialization configured for a node.
    """

    node_revision_id: int = Field(foreign_key="noderevision.id", primary_key=True)
    node_revision: "NodeRevision" = Relationship(
        back_populates="materializations",
    )

    engine_id: int = Field(foreign_key="engine.id", primary_key=True)
    engine: Engine = Relationship()

    name: Optional[str] = Field(primary_key=True)

    # A cron schedule to materialize this node by
    schedule: str

    # Arbitrary config relevant to the materialization engine
    config: Dict = Field(default={}, sa_column=SqlaColumn(JSON))

    # The name of the plugin that handles materialization, if any
    job: str = Field(
        default="MaterializationJob",
        sa_column=SqlaColumn("job", String),
    )


class DruidConf(BaseSQLModel):
    """Druid configuration"""

    granularity: str
    intervals: Optional[List[str]]
    timestamp_column: str
    timestamp_format: Optional[str]
    parse_spec_format: Optional[str]


class GenericCubeConfig(GenericMaterializationConfig):
    """
    Generic cube materialization config needed by any materialization
    choices and engine combinations
    """

    dimensions: Optional[List[str]]
    measures: Optional[Dict[str, List[Dict[str, str]]]]


class DruidCubeConfig(GenericCubeConfig):
    """
    Specific cube materialization implementation with Spark and Druid ingestion and
    optional prefix and/or suffix to include with the materialized entity's name.
    """

    prefix: Optional[str] = ""
    suffix: Optional[str] = ""
    druid: Optional[DruidConf]


class UpsertCubeMaterializationConfig(BaseSQLModel):
    """
    An upsert object for cube materialization configs
    """

    name: Optional[str]
    engine: EngineRef
    config: Union[DruidCubeConfig, GenericCubeConfig]
    schedule: str