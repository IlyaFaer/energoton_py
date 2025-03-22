"""
This sample shows how to set priorities for
tasks, including custom priorities.
"""

from work import ExponentialPriority, NoPriority, Task, custom_priority

# By default, tasks don't have a priority,
# which is equal to the following:
t1 = Task(
    cost=4,
    name="Photo Loading Screen",
    priority=NoPriority(),
)

# Exponential priority provides you with
# the following priority levels:
# - lowest
# - low (1 low task = 2 lowest tasks)
# - normal (1 normal task = 2 low tasks = 4 lowest tasks)
# - high (1 high task = 2 normal tasks = 4 low tasks = 8 lowest tasks)
# - highest (1 highest task = 2 high tasks = 4 normal tasks =
# 8 low tasks = 16 lowest tasks)
#
# Such priority values make energotons sensitive enough
# to really respect the priorities.
t2 = Task(
    cost=4,
    name="Photo Loading Screen",
    priority=ExponentialPriority("high"),
)

# While the exponential priority is good for
# most cases, you may want to create your own
# priority levels to tweak the sensitivity of
# energotons to priorities.
values = {"low": 1, "medium": 5, "high": 10}
CustomPriority = custom_priority(values)

t3 = Task(
    cost=4,
    name="Photo Loading Screen",
    priority=CustomPriority("medium"),
)
