from __future__ import annotations
import logging

log = logging.getLogger(__name__)


class ResidueModification:

    def __init__(self, name: str = None):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return False
