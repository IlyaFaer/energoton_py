class Alternative:
    def __init__(self, id_, *alternatives):
        self.id = id_
        if len(alternatives) <= 1:
            raise ValueError("Alternative relation must have at least two alternatives")

        self.alternatives = alternatives

        for unit in alternatives:
            unit.relations[id_] = self

    @property
    def is_solved(self):
        return any(unit.is_solved for unit in self.alternatives)


class Blocking:
    def __init__(self, id_, blocker, blocked):
        self.id = id_

        self.blocker = blocker
        self.blocked = blocked

        blocked.relations[id_] = self
        blocker.relations[id_] = self

    def drop(self):
        del self.blocked.relations[self.id]
        del self.blocker.relations[self.id]
