"""
The sample shows how to build all possible plans
for a pool of tasks and one energoton.
"""

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from energoton.planner import Planner
from work import Pool, Task

t1 = Task(
    cost=4,
    id_="1",
)
t2 = Task(
    cost=3,
    id_="2",
)
t3 = Task(
    cost=5,
    id_="3",
)
t4 = Task(
    cost=2,
    id_="4",
)

pool = Pool(children=[t1, t2, t3, t4])

e = DeterministicEnergoton(capacity=8)

planner = Planner(pool=pool)
plans = planner.build_plans(energotons=[e])
print("---------DETERMINISTIC All plans:")
for plan in plans:
    print(plan)

print()

e = NonDeterministicEnergoton(capacity=8)

planner = Planner(pool=pool)
plans = planner.build_plans(energotons=[e])
print("---------NON-DETERMINISTIC All plans:")
for plan in plans:
    print(plan)

print(
    """
In this simple case, we're returning all the possible plans.
They are not ordered or sorted in any way - just all
the mathematically possible variants.

You can see practical difference between deterministic and
non-deterministic energotons. While deterministic energoton
proposes you a plan with only two tasks solved:
[
    WorkDone(
        task=Task(
            id_='1',
            cost=4,
        ),
        amount=4,
    ),
    WorkDone(
        task=Task(
            id_='2',
            cost=3,
        ),
        amount=3,
    )
]

Non-deterministic energoton can add a bit more work to the
same plan, and put efforts into the third task:
[
    WorkDone(
        task=Task(
            id_='1',
            cost=4,
        ),
        amount=4,
    ),
    WorkDone(
        task=Task(
            id_='2',
            cost=3,
        ),
        amount=3,
    ),
    WorkDone(
        task=Task(
            id_='3',
            cost=5,
        ),
        amount=1,  # the task is solved partially
    )
]"""
)
