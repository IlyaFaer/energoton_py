from .work_unit import WorkUnit


class Task(WorkUnit):
    def __init__(self, id_, name, cost, priority=1, parent=None, custom_fields={}):
        self.cost = cost
        self.priority = priority

        self.spent = 0

        super().__init__(id_, name, custom_fields, parent)

    def __repr__(self):
        return f"Task(id={self.id}, name='{self.name}')"

    @property
    def is_solved(self):
        return self.spent == self.cost

    @property
    def todo(self):
        return self.cost - self.spent
