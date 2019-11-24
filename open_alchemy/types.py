"""Types shared across modules."""

import dataclasses
import typing

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore

Schema = typing.Dict[str, typing.Any]
Schemas = typing.Dict[str, Schema]
AllOfSpec = typing.List[Schema]


class ModelFactory(Protocol):
    """Defines interface for model factory."""

    def __call__(self, *, name: str) -> typing.Type:
        """Call signature for ModelFactory."""
        ...


# Unique consraint types
ColumnList = typing.List[str]
ColumnListList = typing.List[ColumnList]
Unique = typing.Dict[str, typing.Any]
UniqueList = typing.List[Unique]
AnyUnique = typing.Union[ColumnList, ColumnListList, Unique, UniqueList]
# Index types
Index = typing.Dict[str, typing.Any]
IndexList = typing.List[Index]
AnyIndex = typing.Union[ColumnList, ColumnListList, Index, IndexList]


# Expected format of a column schema
class _ColumnSchemaBase(TypedDict):
    """Base class for column schema."""

    type: str


class ColumnSchema(_ColumnSchemaBase, total=False):
    """Schema for column definitions."""

    format: str
    maxLength: int
    nullable: bool


@dataclasses.dataclass
class ColumnArtifacts:
    """Information required to construct a column."""

    # OpenAPI properties
    type: str
    format: typing.Optional[str] = None
    max_length: typing.Optional[int] = None
    nullable: bool = True

    # Extension properties
    primary_key: typing.Optional[bool] = None
    autoincrement: typing.Optional[bool] = None
    index: typing.Optional[bool] = None
    unique: typing.Optional[bool] = None
    foreign_key: typing.Optional[str] = None
