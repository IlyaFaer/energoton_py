"""
The sample demonstrates how to set relations
between tasks for more complex planning cases.
"""

from energoton import DeterministicEnergoton
from energoton.planner import Planner
from work import Alternative, Blocking, Pool, Task

t1 = Task(
    cost=3,
    id_="1",
)
t2 = Task(
    cost=3,
    id_="2",
)

blocking_rel = Blocking(
    blocker=t1,
    blocked=t2,
)

pool = Pool(children=[t1, t2])

e = DeterministicEnergoton(capacity=8)

planner = Planner(pool=pool)
plans = planner.build_plans(energotons=[e])

print(
    (
        "Planner sees only one plan - to solve t1"
        " (blocker) and then t2 (blocked):"
    )
)
for plan in plans:
    print(plan)

# withdraw the relation
blocking_rel.drop()

Alternative(t1, t2)

planner = Planner(pool=pool)
plans = planner.build_plans(energotons=[e])

print(
    (
        "Planner sees two plans - to solve t1 or "
        "t2, but not both, as they are alternatives:"
    )
)
for plan in plans:
    print(plan)
