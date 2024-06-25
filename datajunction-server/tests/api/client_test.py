"""
Tests for client code generator.
"""
import os
from pathlib import Path

import pytest
from httpx import AsyncClient

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def load_expected_file():
    """
    Loads expected fixture file
    """

    def _load(filename: str):
        expected_path = TEST_DIR / Path("files/client_test")
        with open(expected_path / filename, encoding="utf-8") as fe:
            return fe.read().strip()

    return _load


def trim_trailing_whitespace(string: str) -> str:
    """Trim trailing whitespace on each line"""
    return "\n".join([chunk.rstrip() for chunk in string.split("\n")]).strip()


@pytest.mark.asyncio
async def test_generated_python_client_code_new_source(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Test generating Python client code for creating a new source
    """
    expected = load_expected_file("register_table.txt")
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.repair_order_details"
        "?include_client_setup=false",
    )
    assert trim_trailing_whitespace(response.json()) == expected
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.repair_order_details"
        "?include_client_setup=false&replace_namespace=%7Bnamespace%7D",
    )
    assert trim_trailing_whitespace(response.json()) == expected


@pytest.mark.asyncio
async def test_generated_python_client_code_new_transform(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Test generating Python client code for creating a new transform
    """
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.regional_level_agg"
        "?include_client_setup=false",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file("create_transform.regional_level_agg.txt").strip()
    )
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.regional_level_agg"
        "?include_client_setup=false&replace_namespace=%7Bnamespace%7D",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file(
            "create_transform.regional_level_agg.namespace.txt",
        ).strip()
    )


@pytest.mark.asyncio
async def test_generated_python_client_code_new_dimension(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Test generating Python client code for creating a new dimension
    """
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.repair_order"
        "?include_client_setup=false",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file("create_dimension.repair_order.txt").strip()
    )

    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.repair_order"
        "?include_client_setup=false&replace_namespace=%7Bnamespace%7D",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file("create_dimension.repair_order.namespace.txt").strip()
    )


@pytest.mark.asyncio
async def test_generated_python_client_code_new_metric(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Test generating Python client code for creating a new metric
    """
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.num_repair_orders"
        "?include_client_setup=false",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file("create_metric.num_repair_orders.txt").strip()
    )

    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.num_repair_orders"
        "?include_client_setup=false&replace_namespace=%7Bnamespace%7D",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file("create_metric.num_repair_orders.namespace.txt").strip()
    )


@pytest.mark.asyncio
async def test_generated_python_client_code_new_cube(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Test generating Python client code for creating a new cube
    """
    await client_with_roads.post(
        "/nodes/cube/",
        json={
            "metrics": ["default.num_repair_orders", "default.total_repair_cost"],
            "dimensions": [
                "default.hard_hat.country",
                "default.hard_hat.city",
            ],
            "description": "Cube of various metrics related to repairs",
            "mode": "published",
            "name": "default.repairs_cube",
        },
    )
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.repairs_cube"
        "?include_client_setup=false",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file("create_cube.repairs_cube.txt").strip()
    )
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.repairs_cube"
        "?include_client_setup=false&replace_namespace=%7Bnamespace%7D",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file(
            "create_cube.repairs_cube.namespace.txt",
        ).strip()
    )


@pytest.mark.asyncio
async def test_generated_python_client_code_adding_materialization(
    client_with_query_service_example_loader,
):
    """
    Test that generating python client code for adding materialization works
    """
    custom_client = await client_with_query_service_example_loader(["BASIC"])
    await custom_client.post(
        "/engines/",
        json={
            "name": "spark",
            "version": "2.4.4",
            "dialect": "spark",
        },
    )
    await custom_client.post(
        "/nodes/basic.transform.country_agg/materialization/",
        json={
            "job": "spark_sql",
            "strategy": "full",
            "config": {
                "spark": {},
            },
            "schedule": "0 * * * *",
        },
    )
    response = await custom_client.get(
        "/datajunction-clients/python/add_materialization/"
        "basic.transform.country_agg/spark_sql__full",
    )
    assert (
        response.json()
        == """dj = DJBuilder(DJ_URL)

country_agg = dj.transform(
    "basic.transform.country_agg"
)
materialization = MaterializationConfig(
    job="spark_sql",
    strategy="full",
    schedule="0 * * * *",
    config={
        "spark": {}
    },
)
country_agg.add_materialization(
    materialization
)"""
    )


@pytest.mark.asyncio
async def test_generated_python_client_code_link_dimension(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Test generating Python client code for creating a new dimension
    """
    response = await client_with_roads.get(
        "/datajunction-clients/python/dimension_links/default.repair_orders/"
        "?include_client_setup=false",
    )
    assert (
        response.json().strip()
        == load_expected_file("dimension_links.repair_orders.txt").strip()
    )
    # When replace_namespace is set, verify that the namespaces are replaced in the
    # dimension links' join SQL
    response = await client_with_roads.get(
        "/datajunction-clients/python/dimension_links/default.repair_orders/"
        "?include_client_setup=false&replace_namespace=%7Bnamespace%7D",
    )
    assert (
        response.json().strip()
        == load_expected_file(
            "dimension_links.repair_orders.namespace.txt",
        ).strip()
    )


@pytest.mark.asyncio
async def test_include_client_setup(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Generate create new node python client code with client setup included.
    """
    response = await client_with_roads.get(
        "/datajunction-clients/python/new_node/default.num_repair_orders"
        "?include_client_setup=true",
    )
    assert (
        trim_trailing_whitespace(response.json()).strip()
        == load_expected_file("include_client_setup.txt").strip()
    )


@pytest.mark.asyncio
async def test_export_namespace_as_notebook(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Verify exporting all nodes in a namespace as a notebook.
    """
    response = await client_with_roads.get(
        "/datajunction-clients/python/notebook?namespace=default",
    )
    assert (
        response.headers["content-disposition"] == 'attachment; filename="export.ipynb"'
    )
    notebook = response.json()
    assert len(notebook["cells"]) == 47
    # Intro cell
    assert notebook["cells"][0]["cell_type"] == "markdown"
    assert (
        "## DJ Namespace Export\n\nExported `default`" in notebook["cells"][0]["source"]
    )

    # Client setup cell
    assert notebook["cells"][1]["cell_type"] == "code"
    assert "from datajunction import" in notebook["cells"][1]["source"]

    # Documenting what nodes are being upserted cell
    assert notebook["cells"][2]["cell_type"] == "markdown"
    assert "### Upserting Nodes:" in notebook["cells"][2]["source"]

    # Namespace mapping configuration cell
    assert notebook["cells"][3]["cell_type"] == "code"
    assert (
        notebook["cells"][3]["source"]
        == """# A mapping from current namespaces to new namespaces
# Note: Editing the mapping will result in the nodes under that namespace getting
# copied to the new namespace

NAMESPACE_MAPPING = {
    "default": "default",
}"""
    )

    # Registering table
    assert notebook["cells"][4]["cell_type"] == "code"
    assert (
        notebook["cells"][4]["source"]
        == load_expected_file("register_table.txt").strip()
    )

    # Linking dimensions for table
    assert (
        notebook["cells"][5]["source"]
        == "Linking dimensions for source node `default.repair_order_details`:"
    )
    assert (
        notebook["cells"][6]["source"]
        == load_expected_file(
            "notebook.link_dimension.txt",
        ).strip()
    )

    # Create transform
    assert (
        trim_trailing_whitespace(notebook["cells"][18]["source"])
        == load_expected_file(
            "notebook.create_transform.txt",
        ).strip()
    )


@pytest.mark.asyncio
async def test_export_cube_as_notebook(
    client_with_roads: AsyncClient,
    load_expected_file,  # pylint: disable=redefined-outer-name
):
    """
    Verify exporting all nodes relevant for a cube as a notebook.
    """
    await client_with_roads.post(
        "/nodes/cube/",
        json={
            "metrics": ["default.num_repair_orders", "default.total_repair_cost"],
            "dimensions": [
                "default.hard_hat.country",
                "default.hard_hat.city",
            ],
            "description": "Cube of various metrics related to repairs",
            "mode": "published",
            "name": "default.roads_cube",
        },
    )
    response = await client_with_roads.get(
        "/datajunction-clients/python/notebook?cube=default.roads_cube",
    )
    assert (
        response.headers["content-disposition"] == 'attachment; filename="export.ipynb"'
    )
    notebook = response.json()
    assert len(notebook["cells"]) == 10

    # Intro cell
    assert notebook["cells"][0]["cell_type"] == "markdown"
    assert (
        "## DJ Cube Export\n\nExported `default.roads_cube` v1.0"
        in notebook["cells"][0]["source"]
    )

    # Documenting which nodes are getting exported
    assert (
        notebook["cells"][2]["source"]
        == """### Upserting Nodes:
* default.repair_orders_fact
* default.total_repair_cost
* default.num_repair_orders
* default.roads_cube"""
    )

    # Export first transform
    assert trim_trailing_whitespace(
        notebook["cells"][4]["source"],
    ) == load_expected_file(
        "notebook.create_transform.txt",
    )

    # Include sources and dimensions
    response = await client_with_roads.get(
        "/datajunction-clients/python/notebook?cube=default.roads_cube"
        "&include_sources=true&include_dimensions=true",
    )
    notebook = response.json()
    assert len(notebook["cells"]) == 20
    assert (
        notebook["cells"][2]["source"]
        == """### Upserting Nodes:
* default.repair_order_details
* default.repair_orders
* default.repair_orders_fact
* default.hard_hats
* default.total_repair_cost
* default.num_repair_orders
* default.hard_hat
* default.roads_cube"""
    )
    assert (
        trim_trailing_whitespace(notebook["cells"][19]["source"])
        == load_expected_file(
            "notebook.create_cube.txt",
        ).strip()
    )


@pytest.mark.asyncio
async def test_export_notebook_failures(client_with_roads: AsyncClient):
    """
    Verify that trying to set both cube and namespace when exporting to a notebook will fail
    """
    response = await client_with_roads.get(
        "/datajunction-clients/python/notebook?namespace=default&cube=default.roads_cube",
    )
    assert (
        response.json()["message"]
        == "Can only specify export of either a namespace or a cube."
    )
