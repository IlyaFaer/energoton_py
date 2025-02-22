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

    @property
    def length(self):
        return len(self)

    @property
    def energy_spent(self):
        return sum(t.spent for t in self)

    @property
    def value(self):
        return sum(t.priority.value for t in self)


class Planner(list):
    def __init__(self, energotons, pool, cycles=1):
        self._pool = pool
        self._energotons = energotons
        self._cycles = cycles

        self._plans = []

    def _deduplicate_plans(self, plans):
        unique_plans = []
        for plan in plans:
            plan = Plan(sorted(plan, key=lambda t: t.id))
            if plan not in unique_plans:
                unique_plans.append(plan)

        return unique_plans

    def build_plans(self):
        self._plans = self._energotons[0].build_plans(self._pool)
        return self._plans

    def filter_plans(
        self, ignore_task_order=False, sort_by="value", only_best=False
    ):
        plans = self._plans

        if ignore_task_order:
            plans = self._deduplicate_plans(plans)

        if sort_by in ("value", "energy_spent", "length"):
            plans.sort(key=lambda p: getattr(p, sort_by), reverse=True)

            if only_best:
                plans = self._only_best(plans, sort_by)

        elif sort_by is not None:
            raise ValueError(
                f"'sort_by' argument must be one of: ['value', 'energy_spent', 'length', None]"
            )

        return tuple(plans)

    def _only_best(self, plans, attr):
        i = 1
        while getattr(plans[i], attr) == getattr(plans[0], attr):
            i += 1

        return plans[:i]

    def pool_after_plan(self, plan):
        pool = copy.deepcopy(self._pool)
        for task in plan:
            if task.is_solved:
                pool.pop(task.id)
            else:
                pool.get(task.task.id).spent += task.part_done
                if task.task.is_solved:
                    pool.pop(task.task.id)

            if (
                pool.id != task.parent.id
                and pool.get(task.parent.id).is_solved
            ):
                pool.pop(task.parent.id)

        return pool
