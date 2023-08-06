from __future__ import annotations
import logging

from lipidhandler.residuelist import ResidueList
from lipidhandler.lipidclass import LipidClass
from lipidhandler.residue import Residue
from lipidhandler.dictionaries import CLASS_DEFAULT_MODIFICATION

log = logging.getLogger(__name__)


class Lipid:

    def __init__(self, lipidclass: LipidClass = None, residues: ResidueList = None):
        self.residues = residues
        self.lipidclass = lipidclass
        self._input = None

    def __str__(self) -> str:
        return self.swisslipids_abbreviation()

    def swisslipids_abbreviation(self, summed: bool = False) -> str:
        """
        Return the abbreviation of the lipid in the format preferred by SwissLipids.

        E.g. CE(16:3)

        You can either return the summed residues or multiple residues.

        :arg summed: Summed or multiple residues.
        :return: SwissLipids abbreviation of the lipid.
        """
        if summed:
            first_modification_string = ''
            # TODO understand modification logic and adapt this
            # collect modifications, still unclear what the logic is here
            list_of_modifications = []
            for r in self.residues:
                if r.modification:
                    list_of_modifications.append(r.modification.name)
            # assert that we only have one modification, figure out if mulitple are ok
            if len(list_of_modifications) > 1:
                log.error(self.residues)
                log.error(list_of_modifications)
                raise TypeError("Only one modification per ResidueList allowed")
            # if there is zero or one modifications, continue and pick first one
            if list_of_modifications:
                first_modification_string = list_of_modifications[0]

            return f'{self.lipidclass.name}({first_modification_string}{self.residue_sum().residue_string})'
        else:
            return f"{self.lipidclass.name}({self.residues.residuelist_string})"

    def residue_sum(self) -> Residue:
        """
        Sum up all carbon atoms and double bonds of all residues and return the sum.
        """
        return self.residues.sum()

    def check_consistency(self):
        """
        Check consistency of the Lipid and modify as necessary.
        """
        log.debug(f'Check consistency of {self.swisslipids_abbreviation()}, input was {self._input}')

        # check for modifications depending on class
        if self.lipidclass.name in CLASS_DEFAULT_MODIFICATION:
            default_modification = CLASS_DEFAULT_MODIFICATION[self.lipidclass.name]

            if not self.residues[0].modification == default_modification:
                log.debug(f'Default modification not correct. Expected {default_modification}, found {self.residues[0].modification}')
                self.residues[0].modification = default_modification

    @classmethod
    def parse(cls, string: str) -> Lipid:
        """
        Parse a string represntation of a lipid and create Lipid class.

        :param string: The input string.
        :return: An instance of Lipid
        """
        if string.count('(') > 1 or string.count(')') > 1:
            raise NotImplementedError('alternative chains not implemented')


        # identify abbreviation type
        if '(' in string and ')' in string:
            pass

        # CE 22:4;0
        elif ' ' in string:
            lipid_class_name, residue_string = string.split(' ', 1)

            lipidclass = LipidClass.parse(lipid_class_name)
            residuelist = ResidueList.parse(residue_string)

            lipid = cls(lipidclass, residuelist)
            lipid._input = string

            return lipid


