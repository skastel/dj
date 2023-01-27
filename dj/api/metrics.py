"""
Metric related APIs.
"""

from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, SQLModel, select

from dj.api.queries import save_query_and_run
from dj.config import Settings
from dj.models.node import Node, NodeType
from dj.models.query import QueryWithResults
from dj.sql.build import get_query_for_node
from dj.sql.dag import get_dimensions
from dj.utils import UTCDatetime, get_session, get_settings

router = APIRouter()


class Metric(SQLModel):
    """
    Class for a metric.
    """

    id: int
    name: str
    current_version: str
    description: str = ""

    created_at: UTCDatetime
    updated_at: UTCDatetime

    query: str

    dimensions: List[str]

    @classmethod
    def parse_reference_node(cls, ref_node: Node) -> "Metric":
        """
        Parses a reference node into a metric.
        """

        return cls(
            **ref_node.dict(),
            description=ref_node.current.description,
            updated_at=ref_node.current.updated_at,
            query=ref_node.current.query,
            dimensions=get_dimensions(ref_node),
        )


class TranslatedSQL(SQLModel):
    """
    Class for SQL generated from a given metric.
    """

    database_id: int
    sql: str


def get_metric(session: Session, name: str) -> Node:
    """
    Return a metric node given a node name.
    """
    statement = select(Node).where(Node.name == name)
    try:
        ref_node = session.exec(statement).one()
        if ref_node.type != NodeType.METRIC:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Not a metric node: `{name}`",
            )
    except NoResultFound as exc:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Metric node not found: `{name}`",
        ) from exc
    return ref_node


@router.get("/metrics/", response_model=List[Metric])
def read_metrics(*, session: Session = Depends(get_session)) -> List[Metric]:
    """
    List all available metrics.
    """
    return [
        Metric.parse_reference_node(ref_node)
        for ref_node in (
            session.exec(
                select(Node).where(Node.type == NodeType.METRIC),
            )
        )
    ]


@router.get("/metrics/{name}/", response_model=Metric)
def read_metric(name: str, *, session: Session = Depends(get_session)) -> Metric:
    """
    Return a metric by name.
    """
    ref_node = get_metric(session, name)
    return Metric.parse_reference_node(ref_node)


@router.get("/metrics/{name}/data/", response_model=QueryWithResults)
async def read_metrics_data(
    name: str,
    database_name: Optional[str] = None,
    d: List[str] = Query([]),  # pylint: disable=invalid-name
    f: List[str] = Query([]),  # pylint: disable=invalid-name
    *,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
    response: Response,
    background_tasks: BackgroundTasks,
) -> QueryWithResults:
    """
    Return data for a metric.
    """
    ref_node = get_metric(session, name)
    create_query = await get_query_for_node(
        session,
        ref_node,
        d,
        f,
        database_name,
    )

    return save_query_and_run(
        create_query,
        session,
        settings,
        response,
        background_tasks,
    )


@router.get("/metrics/{name}/sql/", response_model=TranslatedSQL)
async def read_metrics_sql(
    name: str,
    database_name: Optional[str] = None,
    d: List[str] = Query([]),  # pylint: disable=invalid-name
    f: List[str] = Query([]),  # pylint: disable=invalid-name
    *,
    session: Session = Depends(get_session),
) -> TranslatedSQL:
    """
    Return SQL for a metric.

    A database can be optionally specified. If no database is specified the optimal one
    will be used.
    """
    node = get_metric(session, name)
    create_query = await get_query_for_node(session, node, d, f, database_name)

    return TranslatedSQL(
        database_id=create_query.database_id,
        sql=create_query.submitted_query,
    )
