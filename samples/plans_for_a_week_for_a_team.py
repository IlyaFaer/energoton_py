"""
The sample shows how to plan work for an entire team
and for several work cycles.
"""

from energoton import DeterministicEnergoton
from energoton.planner import Planner
from work import Pool, Task

# Say we have 8 tasks.
pool = Pool(name="Sprint, Mar 2025, Week 1")

pool.add(Task(id_="1", cost=6))
pool.add(Task(id_="2", cost=5))
pool.add(Task(id_="3", cost=3))
pool.add(Task(id_="4", cost=7))
pool.add(Task(id_="5", cost=4))
pool.add(Task(id_="6", cost=6))
pool.add(Task(id_="7", cost=5))
pool.add(Task(id_="8", cost=3))

# We have 2 full-time and 1 part-time employees,
# and one of the full-timers is going to
# take a parental leave.

# A full-time employer work every day, 8 hours per day.
e1 = DeterministicEnergoton(capacity=8)

# A full-time employee works only 2 days this week.
e2 = DeterministicEnergoton(capacity=[8, 0, 0, 0, 8])

# Part-time employer works 20 hours per week
# on free schedule, so we don't know at which
# days exactly they'll work (and we don't really
# care).
e3 = DeterministicEnergoton(capacity=[20])

planner = Planner(energotons=[e1, e2, e3], pool=pool)
plans = planner.build_plans(cycles=5)

plans = planner.filter_plans(sort_by="value", only_best=True)
print(f"Built {len(plans)} plans")
