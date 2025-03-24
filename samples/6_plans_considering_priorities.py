"""
The sample demonstrates how to use task
priorities during planning.
"""

from energoton import DeterministicEnergoton
from energoton.planner import Planner
from work import ExponentialPriority, Pool, Task

pool = Pool(name="Sprint, Mar 2025, Week 1")

pool.add(Task(id_="1", cost=4, priority=ExponentialPriority("normal")))
pool.add(Task(id_="2", cost=3, priority=ExponentialPriority("high")))
pool.add(Task(id_="3", cost=1, priority=ExponentialPriority("highest")))
pool.add(Task(id_="4", cost=5, priority=ExponentialPriority("low")))
pool.add(Task(id_="5", cost=2, priority=ExponentialPriority("high")))

e = DeterministicEnergoton(capacity=8)

planner = Planner(energotons=[e], pool=pool)
plans = planner.build_plans()

print(f"The best plan, considering priorities:")
for plan in plans:
    print(plan.value, plan)
