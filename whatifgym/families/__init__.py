"""Task families: templated question generators with reference solutions produced by the oracle."""
from .base import FamilyContext, TaskFamily  # noqa: F401
from .data_change import DataChangeFamily  # noqa: F401
from .new_limit import NewLimitFamily  # noqa: F401

FAMILIES = {DataChangeFamily.name: DataChangeFamily, NewLimitFamily.name: NewLimitFamily}
