"""Task families: templated question generators with reference solutions produced by the oracle.

Eight families so far (the plan lists ten):

======================  =====================================================================  ==================
family                  what the planner asks                                                 DSL part
======================  =====================================================================  ==================
``data_change``         one or two input numbers change; rows added or removed                ``data_changes``
``new_limit``           a cap or floor on the sum of a decision measure over a scope          ``rules`` (absolute)
``relative_rule``       a limit relative to another quantity (ratio, share of total)          ``rules`` (relative)
``objective_change``    what counts as best changes (lexicographic stages, or a new goal)     ``objective``
``fixed_decision``      part of the plan is committed; optimise the rest                      ``fixed_decisions``
``relax_remove``        a limit of the model no longer applies (in full or over a scope)      ``relax``
``logical_rule``        either-or: never both, none or a minimum batch, if-then, k of n       ``logic``
``under_specified``     the question lacks what is needed; ask first, then answer             ``ask`` then any
======================  =====================================================================  ==================
"""
from .base import FamilyContext, TaskFamily  # noqa: F401
from .data_change import DataChangeFamily  # noqa: F401
from .fixed_decision import FixedDecisionFamily  # noqa: F401
from .logical_rule import LogicalRuleFamily  # noqa: F401
from .new_limit import NewLimitFamily  # noqa: F401
from .objective_change import ObjectiveChangeFamily  # noqa: F401
from .relative_rule import RelativeRuleFamily  # noqa: F401
from .relax_remove import RelaxRemoveFamily  # noqa: F401
from .under_specified import UnderSpecifiedFamily  # noqa: F401

FAMILIES = {fam.name: fam for fam in (DataChangeFamily, NewLimitFamily, RelativeRuleFamily, ObjectiveChangeFamily,
                                      FixedDecisionFamily, RelaxRemoveFamily, LogicalRuleFamily, UnderSpecifiedFamily)}
