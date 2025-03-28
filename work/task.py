from .work_unit import Priority, WorkDone, WorkUnit


class Task(WorkUnit):
    def __init__(
        self,
        cost,
        custom_fields={},
        parent=None,
        priority=Priority("normal"),
        id_=None,
        name=None,
    ):
        self._work_done = []
        self.cost = cost

        super().__init__(custom_fields, parent, priority, id_, name)

    def __repr__(self):
        return f"Task(id_='{self.id}', name='{self.name}', cost={self.cost})"

    @property
    def dry(self):
        return {
            "id": self.id,
            "cost": self.cost,
            "spent": self.spent,
            "relations": self.relations,
            "priority": self.priority,
        }

    @property
    def spent(self):
        return sum(w.amount for w in self._work_done)

    @property
    def is_solved(self):
        return self.spent == self.cost

    @property
    def todo(self):
        return self.cost - self.spent

    def drop_work_done(self, energy_spent):
        self._work_done.remove(energy_spent)

    def work_done(self, energy_spent, energoton, cycle=1):
        work_done = WorkDone(
            str(self.id) + "-work_done-" + str(len(self._work_done) + 1),
            self,
            energy_spent,
            energoton,
            cycle,
        )
        self._work_done.append(work_done)
        return work_done
