"""Basic functionality classes."""

import uuid


class Id:
    """
    Object id functionality. Used by energotons,
    pools, relations, work units and tasks.

    Args:
        id_ (Optional[Union[str, uuid.UUID]]):
            Explicit object id. If not provided,
            a UUID is generated.
    """

    def __init__(self, id_=None):
        self._id = id_ or uuid.uuid4()

    def __eq__(self, other):
        """Magic method for the equality operator.

        Args:
            other (Any): Object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        return self.id == other.id

    def __hash__(self):
        """Magic method for the hash function.

        Returns:
            int: Object hash.
        """
        return hash(self.id)

    @property
    def id(self):
        """Object id.

        Returns:
            Union[str, uuid.UUID]: Object id.
        """
        return self._id

    @id.setter
    def id(self, _):
        """Changing an object id is not allowed.

        Raises:
            ValueError: Object id is immutable.
        """
        raise ValueError(f"Object '{self.id}' id is immutable")
