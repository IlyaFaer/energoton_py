import uuid


class IdMixin:
    def __init__(self, id_=None):
        self._id = id_ or uuid.uuid4()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _):
        raise ValueError(f"Object '{self.id}' id is immutable")
