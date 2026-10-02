"""Registry of base models. Add a model by importing its class here."""
from __future__ import annotations

from .base import BaseModel


def _registry() -> dict[str, type[BaseModel]]:
    # Imported lazily so that `import whatifgym` stays cheap and solver-free.
    from .models.factory_planning.model import FactoryPlanning
    from .models.multiple_knapsack.model import MultipleKnapsack
    from .models.wedding_seating.model import WeddingSeating

    classes = [FactoryPlanning, MultipleKnapsack, WeddingSeating]
    return {cls.name: cls for cls in classes}


def list_models() -> list[str]:
    return sorted(_registry())


def get_model(name: str) -> BaseModel:
    reg = _registry()
    if name not in reg:
        raise KeyError(f"unknown model {name!r}; available: {sorted(reg)}")
    return reg[name]()
