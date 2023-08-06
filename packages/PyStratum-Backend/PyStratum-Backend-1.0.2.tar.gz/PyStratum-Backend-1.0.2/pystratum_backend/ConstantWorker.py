from abc import ABC


class ConstantWorker(ABC):
    """
    Interface for classes that implement the actual execution of the constant command.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self) -> int:
        """
        Does the actual execution of the constant command for the backend. Returns 0 on success. Otherwise returns
        nonzero.

        :rtype: int
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
