from lipidhandler.lipidlist import LipidList
from lipidhandler.externalapis.apimodel import ExternalApi


class SwissLipidsApi(ExternalApi):

    def __init__(self):
        super(SwissLipidsApi, self).__init__()

    def search(self, search_term) -> LipidList:
        lipidlist = LipidList()

        return lipidlist