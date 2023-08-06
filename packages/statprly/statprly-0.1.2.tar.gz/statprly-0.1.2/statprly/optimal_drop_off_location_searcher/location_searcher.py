"""
Provide an implementation of the optimal drop-off location searcher.
"""
from statprly.optimal_drop_off_location_searcher.interfaces import BaseOptimalDropOffLocationSearcher


class OptimalDropOffLocationSearcher(BaseOptimalDropOffLocationSearcher):
    """
    Implementation of the optimal drop-off location searcher.
    """

    def __init__(self, loss):
        self.loss = loss

    def get_optimal_location_index(self, heatmap: list) -> int:
        """
        Get optimal location for sending a help to a person.

        :param heatmap: histogram of non-normalized probability location of the person.
        :return: optimal location index.
        """
        optimal_heat_condition = sum(heatmap) / 2
        optimal_heat = 0
        for i, heat in enumerate(heatmap):
            if optimal_heat >= optimal_heat_condition:
                return i - 1

            optimal_heat += heat
