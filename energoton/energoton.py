from base import Id
from work import WorkDone, Blocking
from .planner import Plan


class Energoton(Id):
    def __init__(self, capacity, id_=None, name=None):
        self.name = name
        self._capacity = capacity
        self.energy_left = self.next_charge

        self.pool = None
        self._dry_pool = None

        super().__init__(id_)

    def __eq__(self, other):
        return self.id == other.id

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
        if plans:
            if plan.calc_value() < plans[0].value:
                return

            sorted_plan = Plan(sorted(plan, key=lambda w: w.task.id))
            sorted_plan.commit()

            if sorted_plan.value > plans[0].value:
                plans.clear()
            elif sorted_plan in plans:
                return
        else:
            sorted_plan = Plan(sorted(plan, key=lambda w: w.task.id))
            sorted_plan.commit()

        plans.append(sorted_plan)

    def _build_plans(self, task, plan, tasks, plans, cycle):
        if task:
            work_done = self.work(task, cycle)
            plan.append(work_done)
            if task["cost"] == task["spent"]:
                tasks.remove(task)

        if self.energy_left == 0:
            self._commit_plan(plan, plans)
        else:
            can_continue = False
            for t in tasks:
                if self.can_solve(t):
                    self._build_plans(t, plan, tasks, plans, cycle)
                    can_continue = True

            if not can_continue:
                self._commit_plan(plan, plans)

        if task:
            if task["cost"] == task["spent"]:
                tasks.append(task)

            del plan[-1]

            self.energy_left += work_done.amount
            task["spent"] -= work_done.amount

    def build_plans(self, dry_pool, cycle=1, plan=None):
        self._dry_pool = dry_pool

        plans = []
        self._build_plans(
            task=None,
            plan=plan or Plan(),
            tasks=list(dry_pool.values()),
            plans=plans,
            cycle=cycle,
        )
        return plans

    def work(self, task, cycle=1):
        energy_spent = min(self.energy_left, task["cost"] - task["spent"])
        self.energy_left -= energy_spent

        task["spent"] += energy_spent

        return WorkDone(
            self.pool.children[task["id"]],
            energy_spent,
            self,
            cycle,
        )

    def _is_actual(self, task_id):
        if not self.pool.children[task_id].relations:
            return True

        for rel in self.pool.children[task_id].relations.values():
            if isinstance(rel, Blocking):
                if rel.blocked.id == task_id:
                    dry = self._dry_pool[rel.blocker.id]
                    if dry["spent"] < dry["cost"]:
                        return False
            else:
                for alt in rel.alternatives:
                    dry = self._dry_pool[alt.id]
                    if dry["spent"] == dry["cost"]:
                        return False

        return True


class DeterministicEnergoton(Energoton):
    def can_solve(self, task):
        return self.energy_left >= task["cost"] - task[
            "spent"
        ] and self._is_actual(task["id"])


class NonDeterministicEnergoton(Energoton):
    def can_solve(self, task):
        return self._is_actual(task["id"])
