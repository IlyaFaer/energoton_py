import copy
from work import Pool


class Plan(list):
    def __len__(self):
        count = 0
        for t in self:
            if isinstance(t, Pool):
                count += len(t.flat_tasks())
            else:
                count += 1
        return count

    def __eq__(self, other):
        return self.dry == other.dry

    @property
    def dry(self):
        return tuple([w.dry for w in self])

    @property
    def energy_spent(self):
        return sum(work.amount for work in self)

    @property
    def value(self):
        return sum(t.task.priority.value for t in self)


class Planner:
    """
    Planner builds plans for the given pool
    and provides methods to analyze them.

    NOTE: On init, Planner makes a deep copy
    of the given pool. It sticks the planner
    to the pool, and allows to re-use the pool
    in multiple planners (e.g. you have 2 teams and
    you want to compare how they'll handle the same
    pool of tasks, running planners in parallel).

    Args:
        pool (work.pool.Pool):
            The pool of tasks to be solved.
    """

    def __init__(self, pool):
        if len(pool) == 0:
            raise ValueError(
                f"The given pool {pool.id} - {pool.name} is empty."
            )

        self._pool = copy.deepcopy(pool)
        self._dry_pool = self._pool.dry

        self._plans = []

    def build_plans(self, energotons, cycles=1):
        self._plans = []

        for c in range(cycles):
            for e in energotons:
                if self._plans == []:
                    self._plans = e.build_plans(
                        self._dry_pool, self._pool, c + 1
                    )
                else:
                    new_plans = []
                    for plan in self._plans:
                        for new_plan in e.build_plans(
                            self.dry_pool_after_plan(plan),
                            self._pool,
                            c + 1,
                            plan,
                        ):
                            if new_plan not in new_plans:
                                new_plans.append(new_plan)

                    self._plans = new_plans

                e.recharge()

        return tuple(self._plans)

    def pool_after_plan(self, plan):
        pool = copy.deepcopy(self._pool)

        for work_done in plan:
            pool.get(work_done.task.id).work_done.append(work_done)

        return pool

    def dry_pool_after_plan(self, plan):
        pool = copy.deepcopy(self._dry_pool)

        to_del = []
        for work_done in plan:
            pool[work_done.task.id]["spent"] += work_done.amount
            if (
                pool[work_done.task.id]["spent"]
                == pool[work_done.task.id]["cost"]
            ):
                to_del.append(work_done.task.id)

        for t in to_del:
            del pool[t]

        return pool

    @staticmethod
    def by_cycles(plans):
        by_cycles = []
        for plan in plans:
            new_plan = {}
            for work_done in plan:
                if work_done.cycle not in new_plan:
                    new_plan[work_done.cycle] = []

                new_plan[work_done.cycle].append(work_done)

            by_cycles.append(new_plan)

        return by_cycles

    @staticmethod
    def by_assignees(plans):
        by_assignees = []
        for plan in plans:
            new_plan = {}
            for work_done in plan:
                as_id = work_done.assignee.id

                if as_id not in new_plan:
                    new_plan[as_id] = []

                new_plan[as_id].append(work_done)

            by_assignees.append(new_plan)

        return by_assignees
