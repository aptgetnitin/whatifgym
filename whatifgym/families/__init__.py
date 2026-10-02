"""Task families: templated question generators with reference solutions produced by the oracle."""
from .data_change import DataChangeFamily  # noqa: F401

FAMILIES = {DataChangeFamily.name: DataChangeFamily}
