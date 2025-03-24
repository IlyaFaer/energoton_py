import copy

from base import Id
from .planner import Plan


class Energoton(Id):
    def __init__(self, capacity, id_=None, name=None):
        self.name = name
        self._capacity = capacity
        self.energy_left = self.next_charge

        super().__init__(id_)

    @property
    def capacity(self):
        return self._capacity

    @property
    def next_charge(self):
        if isinstance(self._capacity, int):
            return self._capacity

        if isinstance(self._capacity, list):
            if len(self._capacity) == 0:
                return 0

            return self._capacity.pop(0)

    def recharge(self):
        self.energy_left = self.next_charge

    def _commit_plan(self, plan, plans):
        sorted_plan = Plan(sorted(plan, key=lambda w: w.task.id))
        if plans:
            if sorted_plan in plans:
                return

            if sorted_plan.value < plans[0].value:
                return

            if sorted_plan.value > plans[0].value:
                plans.clear()

        plans.append(sorted_plan)

    def _build_plans(self, task, plan, tasks, plans, cycle):
        if task is not None:
            work_done = self.work(task, cycle)
            plan.append(work_done)
            if task.is_solved:
                tasks.remove(task)

        can_continue = False
        for t in copy.copy(tasks):
            if self.can_solve(t):
                self._build_plans(t, plan, tasks, plans, cycle)
                can_continue = True

        if not can_continue:
            self._commit_plan(plan, plans)

        if task is not None:
            if task.is_solved:
                tasks.append(task)

            plan.remove(work_done)
            self.energy_left += work_done.amount

            task.drop_work_done(work_done)

    def build_plans(self, pool, cycle=1, plan=None):
        plans = []
        self._build_plans(
            task=None,
            plan=plan or Plan(),
            tasks=pool.flat_tasks(),
            plans=plans,
            cycle=cycle,
        )
        return plans

    def work(self, task, cycle=1):
        energy_spent = min(self.energy_left, task.todo)
        self.energy_left -= energy_spent
        work_done = task.work_done(energy_spent, self, cycle)

        return work_done


class DeterministicEnergoton(Energoton):
    def can_solve(self, task):
        if (
            self.energy_left > 0
            and self.energy_left >= task.todo
            and not task.is_blocked
            and task.is_actual
        ):
            return True
        return False


class NonDeterministicEnergoton(Energoton):
    def can_solve(self, task):
        if self.energy_left > 0 and not task.is_blocked and task.is_actual:
            return True
        return False
