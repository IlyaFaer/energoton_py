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

    def build_plans(self, cycles=1):
        for c in range(cycles):
            for e in self._energotons:
                if self._plans == []:
                    self._plans = e.build_plans(self._pool, c + 1)
                else:
                    new_plans = []
                    for plan in self._plans:
                        new_plans.extend(
                            e.build_plans(
                                self.pool_after_plan(plan), c + 1, plan
                            )
                        )
                    self._plans = new_plans

                e.recharge()

        return tuple(self._plans)

    def pool_after_plan(self, plan):
        pool = copy.deepcopy(self._pool)
        tasks = pool.as_dict

        for work_done in plan:
            tasks[work_done.task.id]._work_done.append(work_done)

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
