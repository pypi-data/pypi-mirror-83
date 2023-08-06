from abc import ABC
from typing import List, Optional


class RoutineLoaderWorker(ABC):
    """
    Interface for classes that implement the actual execution of the routine loader command.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, file_names: Optional[List[str]] = None) -> int:
        """
        Does the actual execution of the routine loader command for the backend. Returns 0 on success. Otherwise
        returns nonzero.

        :param list[str]|None file_names: The sources that must be loaded. If none all sources (if required) will
                                          loaded.

        :rtype: int
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
