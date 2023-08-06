"""
Provide interfaces for monochrome digits recognition.
"""
from abc import (
    ABC,
    abstractmethod,
)


class BaseOptimalDropOffLocationSearcher(ABC):
    """
    Implementation of the basic location searcher.
    """

    @abstractmethod
    def get_optimal_location_index(self, heatmap: list) -> int:
        """
        Get optimal location for sending a help to a person.

        :param heatmap: histogram of non-normalized probability location of the person.
        :return: optimal location index.
        """
