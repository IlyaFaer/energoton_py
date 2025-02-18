from base.mixins import IdMixin


class Alternative(IdMixin):
    def __init__(self, *alternatives, id_=None):
        super().__init__(id_)

        if len(alternatives) <= 1:
            raise ValueError(
                "Alternative relation must have at least two alternatives."
            )

        self.alternatives = alternatives

        for unit in alternatives:
            unit.relations[self.id] = self

    @property
    def is_solved(self):
        return any(unit.is_solved for unit in self.alternatives)


class Blocking(IdMixin):
    def __init__(self, blocker, blocked, id_=None):
        super().__init__(id_)

        self.blocker = blocker
        self.blocked = blocked

        blocked.relations[self.id] = self
        blocker.relations[self.id] = self

    def drop(self):
        del self.blocked.relations[self.id]
        del self.blocker.relations[self.id]
