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
        self.id = id_ or uuid.uuid4()

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
