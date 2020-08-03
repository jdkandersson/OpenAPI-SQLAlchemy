"""Tests for foreign key helper."""

import pytest

from open_alchemy.helpers import foreign_key
from open_alchemy.helpers import relationship


@pytest.mark.parametrize(
    "type_, schema, schemas, expected_column_name",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            "id",
            id="many-to-one not defined",
        ),
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-foreign-key-column": "name"}},
            "name",
            id="many-to-one defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-uselist": False}},
            "id",
            id="one-to-one not defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-foreign-key-column": "name", "x-uselist": False}},
            "name",
            id="one-to-one defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            "id",
            id="one-to-many not defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-foreign-key-column": "name"}},
            "name",
            id="one-to-many defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
            {"RefSchema": {"x-foreign-key-column": "name"}},
            "name",
            id="allOf one-to-many defined",
        ),
    ],
)
@pytest.mark.helper
def test_calculate_column_name(type_, schema, schemas, expected_column_name):
    """
    GIVEN relationship type, schema, schemas and expected column name
    WHEN calculate_column_name is called with the type, schema and schemas
    THEN the expected foreign key column name is returned.
    """
    returned_name = foreign_key.calculate_column_name(
        type_=type_, property_schema=schema, schemas=schemas
    )

    assert returned_name == expected_column_name


@pytest.mark.parametrize(
    "type_, parent_schema, property_schema, schemas, expected_schema",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"parent_key": "parent value"},
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            {"ref_key": "ref value"},
            id="one-to-many",
        ),
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"parent_key": "parent value"},
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"ref_key": "ref value"}},
            {"ref_key": "ref value"},
            id="one-to-many allOf",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            {"parent_key": "parent value"},
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            {"ref_key": "ref value"},
            id="one-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"parent_key": "parent value"},
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"ref_key": "ref value"}},
            {"parent_key": "parent value"},
            id="many-to-one",
        ),
    ],
)
@pytest.mark.helper
def test_get_target_schema(
    type_, parent_schema, property_schema, schemas, expected_schema
):
    """
    GIVEN relationship type, parent and property schema, schemas and expected schema
    WHEN get_target_schema is called with the type, parent and property schema and
        schemas
    THEN the expected schema is returned.
    """
    returned_schema = foreign_key.get_target_schema(
        type_=type_,
        parent_schema=parent_schema,
        property_schema=property_schema,
        schemas=schemas,
    )

    assert returned_schema == expected_schema


@pytest.mark.parametrize(
    "type_, column_name, property_name, schema, schemas, expected_prop_name",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            "column_1",
            "prop_1",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            "prop_1_column_1",
            id="many-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            "column_1",
            "prop_1",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-uselist": False}},
            "prop_1_column_1",
            id="one-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            "column_1",
            "prop_1",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-tablename": "ref_schema"}},
            "ref_schema_prop_1_column_1",
            id="one-to-many not defined",
        ),
    ],
)
@pytest.mark.helper
def test_calculate_prop_name(
    type_, column_name, property_name, schema, schemas, expected_prop_name
):
    """
    GIVEN relationship type, schema, schemas and expected prop name
    WHEN calculate_prop_name is called with the type, schema and schemas
    THEN the expected foreign key prop name is returned.
    """
    returned_name = foreign_key.calculate_prop_name(
        type_=type_,
        column_name=column_name,
        property_name=property_name,
        target_schema=schema,
        schemas=schemas,
    )

    assert returned_name == expected_prop_name


@pytest.mark.helper
def test_calculate_foreign_key():
    """
    GIVEN the target schema and foreign key column name
    WHEN calculate_foreign_key is called with target schema and foreign key column name
    THEN the expected foreign key is returned.
    """
    target_schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"x-tablename": "table_1"}}

    returned_key = foreign_key.calculate_foreign_key(
        foreign_key_column_name="fk_column",
        target_schema=target_schema,
        schemas=schemas,
    )

    assert returned_key == "table_1.fk_column"
