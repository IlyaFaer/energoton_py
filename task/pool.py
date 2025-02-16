from .work_unit import WorkUnit


class Pool(WorkUnit):
    def __init__(self, id_, name, parent=None, children=[], custom_fields={}):
        self.children = {}
        for c in children:
            c.parent = self
            if c.id in self.children:
                raise ValueError(
                    f"Child '{c.name}' with id '{c.id}' already exists in the pool {self.name}."
                )

            self.children[c.id] = c

        super().__init__(id_, name, custom_fields, parent)

    def __iter__(self):
        return iter(self.children.values())

    def __repr__(self):
        return f"Pool(id={self.id}, name={self.name})"

    def __len__(self):
        return len(self.children)

    def get(self, child_id):
        return self.children[child_id]

    def add(self, child):
        if child.id in self.children:
            raise ValueError(
                f"Child with id '{child.id}' already exists in the pool {self.name}."
            )

        child.parent = self
        self.children[child.id] = child

    def pop(self, child_id):
        self.children[child_id].parent = None
        del self.children[child_id]

    @property
    def is_solved(self):
        for c in self.children.values():
            if not c.is_solved:
                return False

        return True

    @property
    def done(self):
        return list(filter(lambda c: c.is_solved, self.children.values()))

    @property
    def todo(self):
        return list(filter(lambda c: not c.is_solved, self.children.values()))

    def flat_tasks(self):
        tasks = []
        for c in self.children.values():
            if isinstance(c, Pool):
                tasks.extend(c.flat_tasks())
            else:
                if not c.is_solved:
                    tasks.append(c)

        return tasks
