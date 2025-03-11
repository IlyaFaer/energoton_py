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
        return sum(work.amount for work in self)

    @property
    def value(self):
        return sum(t.task.priority.value for t in self)


class Planner(list):
    def __init__(self, energotons, pool):
        self._pool = pool
        self._energotons = energotons

        self._plans = []

    def _deduplicate_plans(self, plans):
        unique_plans = []
        for plan in plans:
            plan = Plan(sorted(plan, key=lambda t: t.id))
            if plan not in unique_plans:
                unique_plans.append(plan)

        return unique_plans

    def build_plans(self):
        for e in self._energotons:
            if self._plans == []:
                self._plans = e.build_plans(self._pool)
            else:
                new_plans = []
                for plan in self._plans:
                    new_plans.extend(
                        e.build_plans(self.pool_after_plans([plan]), plan)
                    )
                self._plans = new_plans

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
        while getattr(plans[i], attr) == getattr(
            plans[0], attr
        ) and i + 1 < len(plans):
            i += 1

        return plans[:i]

    def pool_after_plans(self, plans):
        pool = copy.deepcopy(self._pool)
        tasks = pool.as_dict

        for plan in plans:
            for work_done in plan:
                tasks[work_done.task.id]._work_done.append(work_done)

        return pool
