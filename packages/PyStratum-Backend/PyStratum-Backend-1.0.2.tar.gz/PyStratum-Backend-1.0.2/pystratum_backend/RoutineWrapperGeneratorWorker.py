from abc import ABC


class RoutineWrapperGeneratorWorker(ABC):
    """
    Interface for classes that implement the actual execution of the routine wrapper generator command.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self) -> int:
        """
        Does the actual execution of the routine wrapper generator command for the backend. Returns 0 on success.
        Otherwise returns nonzero.

        :rtype: int
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
