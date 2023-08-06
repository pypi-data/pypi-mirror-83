import logging
from typing import List

from lipidhandler.lipid import Lipid

log = logging.getLogger(__name__)


class LipidList:
    """
    For now this is simply a container for a list of Lipid objects.

    Various aggregation methods and summaries seem to be on the roadmap.
    """

    def __init__(self, lipids: List[Lipid] = None):
        if lipids:
            self.lipids = lipids
        else:
            self.lipids = []

    def __iter__(self):
        return iter(self.lipids)

    def __len__(self):
        return len(self.lipids)

    def append(self, item) -> None:
        if isinstance(item, Lipid):
            self.lipids.append(item)
        else:
            raise TypeError('Not of type Lipid')
