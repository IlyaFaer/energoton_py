"""This sample shows how to init energotons.

Usually, you do not manipulate energotons
directly. You only need to init them and
pass them into a planner.
"""

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from work import Task

t = Task(cost=12)

# Deterministic energoton is a transaction type
# of worker. It solves a tasks, only if it has
# enough energy to do it.
de = DeterministicEnergoton(
    capacity=8,
    name="Deterministic Energoton 1",
)

# Amount of energy left.
print(de.energy_left)

# Can't solve a task with cost higher than
# energy left.
print("Deterministic can solve: ", de.can_solve(t))

# Non-deterministic energoton can solve a task
# partially, putting the energy left into
# the task as a contribution.
nde = NonDeterministicEnergoton(
    capacity=8,
    name="Non-Deterministic Energoton 1",
)

print("Non-deterministic can solve: ", nde.can_solve(t))

# Energoton can be charged in several ways.
#
# If you put an `int` as a capacity, then
# the energoton will be charged with this
# amount of energy on every recharge.
de = DeterministicEnergoton(capacity=8)

# If you put a list of `int` as a capacity,
# the energoton will be charged with those
# amounts of energy one by one.
de = DeterministicEnergoton(capacity=[8, 4, 2])

print("1st cycle charge: ", de.energy_left)

de.recharge()
print("2nd cycle charge: ", de.energy_left)

de.recharge()
print("3rd cycle charge: ", de.energy_left)

# If a charge is 0, then the energoton will
# skip working during the related cycle.
de = DeterministicEnergoton(capacity=[8, 0, 2])
