from __future__ import annotations
import logging
import re

from lipidhandler.residuemodification import ResidueModification

log = logging.getLogger(__name__)


class Residue:

    def __init__(self, carbon_atoms: int = None, double_bonds: int = None, oxidation: int = None,
                 modification: ResidueModification = None):
        self.carbon_atoms = carbon_atoms
        self.double_bonds = double_bonds
        self.oxidation = oxidation
        self.modification = modification

    @property
    def residue_string(self) -> str:
        """
        Return string of the residue.

        :return: String of the residue.
        """
        base_string = f'{self.carbon_atoms}:{self.double_bonds}'
        if self.modification:
            base_string = f'{self.modification.name}{base_string}'
        if self.oxidation:
            base_string = f'{base_string};{self.oxidation}'
        return base_string

    @classmethod
    def parse(cls, string: str) -> Residue:
        """
        Parse a string to create Residue. This will fail if a string with more than one residue is
        passed, the ResidueList is the default entrypoint.

        :param string:
        :return:
        """

        # get modifications
        modification = False
        # match if string does not start with digit
        if not re.match('^[0-9]', string):
            # get index of first digit
            index_first_digit = re.search('[0-9]', string).span()[0]
            prefix = string[:index_first_digit]
            modification = ResidueModification(prefix)
            string = string[index_first_digit:]


        log.debug(string)
        chain_def = string.split(';')[0]
        carbon_atoms, double_bonds = chain_def.split(':')

        if ';' in string:
            oxidation = int(string.split(';')[1])
        else:
            oxidation = None

        return cls(int(carbon_atoms), int(double_bonds), oxidation, modification)
