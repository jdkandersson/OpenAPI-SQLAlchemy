"""Retrieve artifacts for a JSON property."""

import copy

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema
) -> types.JsonPropertyArtifacts:
    """
    Retrieve the artifacts for a JSON property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the JSON property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    schema = copy.deepcopy(
        oa_helpers.schema.prepare_deep(schema=schema, schemas=schemas)
    )

    nullable = oa_helpers.peek.nullable(schema=schema, schemas=schemas)

    description = oa_helpers.peek.description(schema=schema, schemas=schemas)

    read_only = oa_helpers.peek.read_only(schema=schema, schemas=schemas)
    write_only = oa_helpers.peek.write_only(schema=schema, schemas=schemas)

    primary_key = oa_helpers.peek.primary_key(schema=schema, schemas=schemas)
    index = oa_helpers.peek.index(schema=schema, schemas=schemas)
    unique = oa_helpers.peek.unique(schema=schema, schemas=schemas)

    foreign_key = oa_helpers.peek.foreign_key(schema=schema, schemas=schemas)

    kwargs = oa_helpers.peek.kwargs(schema=schema, schemas=schemas)
    foreign_key_kwargs = oa_helpers.peek.foreign_key_kwargs(
        schema=schema, schemas=schemas
    )

    # Remove extension properties from schema
    properties = [
        "x-primary-key",
        "x-index",
        "x-unique",
        "x-foreign-key",
        "x-kwargs",
        "x-foreign-key-kwargs",
    ]
    for prop in properties:
        if prop not in schema:
            continue
        del schema[prop]

    return types.JsonPropertyArtifacts(
        type_=helpers.property_.type_.Type.JSON,
        schema=schema,
        open_api=types.OpenApiJsonPropertyArtifacts(
            nullable=nullable,
            description=description,
            read_only=read_only,
            write_only=write_only,
        ),
        extension=types.ExtensionJsonPropertyArtifacts(
            primary_key=primary_key,
            index=index,
            unique=unique,
            foreign_key=foreign_key,
            kwargs=kwargs,
            foreign_key_kwargs=foreign_key_kwargs,
        ),
    )
