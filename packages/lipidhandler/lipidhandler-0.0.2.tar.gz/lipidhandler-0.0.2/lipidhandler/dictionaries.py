from lipidhandler.residuemodification import ResidueModification

##############################################################
# A collection of mapping dictionaries
##############################################################


PREFERRED_CLASS = {
    'TAG': 'TG',
    'DAG': 'DG'
}

# TODO understand modifications and figure out if a default makes sense
#  or if we should output multiple Lipids if modification is not known
CLASS_DEFAULT_MODIFICATION = {
    'Cer': ResidueModification('d'),
    'SM': ResidueModification('d'),
    'HexCer': ResidueModification('d')
}
