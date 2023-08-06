import logging

from lipidhandler.lipidlist import LipidList

log = logging.getLogger(__name__)


class ExternalApi:

    def __init__(self):
        pass

    def search(self, search_term) -> LipidList:
        """
        Use the external API to search for a term and return a LipidList.

        :param search_term: The Search term.
        :return: A LipidList
        """
        raise NotImplementedError
