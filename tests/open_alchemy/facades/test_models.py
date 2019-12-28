"""Tests for models facade."""

from unittest import mock

import pytest

from open_alchemy.facades import models


@pytest.mark.facade
def test_get_base(mocked_models):
    """
    GIVEN mocked models
    WHEN get_base is called
    THEN the mocked_models.Base is returned.
    """
    base = models.get_base()

    assert base == mocked_models.Base


@pytest.mark.facade
def test_set_association(mocked_models):
    """
    GIVEN mocked models, mock table and name
    WHEN set_association is called with the table and name
    THEN the table is set as an attribute on the models with the name.
    """
    name = "association_1"
    table = mock.MagicMock()

    models.set_association(table=table, name=name)

    assert getattr(mocked_models, name) == table


@pytest.mark.facade
def test_get_model(mocked_models):
    """
    GIVE mocked models and name
    WHEN get_model is called with the name
    THEN the models attribute with that name is returned.
    """
    name = "Model"

    model = models.get_model(name=name)

    assert model == getattr(mocked_models, name)


@pytest.mark.facade
def test_get_not_defined(mocked_models):
    """
    GIVE mocked models without model and name
    WHEN get_model is called with the name
    THEN None is returned.
    """
    name = "Model"
    del mocked_models.Model

    model = models.get_model(name=name)

    assert model is None


@pytest.mark.facade
def test_set_model(mocked_models):
    """
    GIVE mocked models, mock model and name
    WHEN set_model is called with the model and name
    THEN the model is set as an attribute on the models with the name.
    """
    model = mock.MagicMock()
    name = "Model"

    models.set_model(model=model, name=name)

    assert getattr(mocked_models, name) == model


@pytest.mark.parametrize(
    "schema, expected_schema",
    [
        ({}, {"x-backrefs": [{"type": "object", "x-de-$ref": "RefSchema"}]}),
        (
            {"x-backrefs": []},
            {"x-backrefs": [{"type": "object", "x-de-$ref": "RefSchema"}]},
        ),
        (
            {"x-backrefs": [{"type": "object", "x-de-$ref": "RefSchema1"}]},
            {
                "x-backrefs": [
                    {"type": "object", "x-de-$ref": "RefSchema1"},
                    {"type": "object", "x-de-$ref": "RefSchema"},
                ]
            },
        ),
        (
            {
                "x-backrefs": [
                    {"type": "object", "x-de-$ref": "RefSchema1"},
                    {"type": "object", "x-de-$ref": "RefSchema2"},
                ]
            },
            {
                "x-backrefs": [
                    {"type": "object", "x-de-$ref": "RefSchema1"},
                    {"type": "object", "x-de-$ref": "RefSchema2"},
                    {"type": "object", "x-de-$ref": "RefSchema"},
                ]
            },
        ),
    ],
    ids=[
        "x-backrefs missing",
        "x-backrefs empty",
        "x-backrefs single",
        "x-backrefs multiple",
    ],
)
@pytest.mark.facade
def test_add_backref_to_schema(schema, expected_schema):
    """
    GIVEN given schema and backref to add
    WHEN _add_backref_to_schema is called with the schema and backref to add
    THEN the backref is added to the schema.
    """
    # pylint: disable=protected-access
    backref = {"type": "object", "x-de-$ref": "RefSchema"}

    models._add_backref_to_schema(schema=schema, backref=backref)

    assert schema == expected_schema
