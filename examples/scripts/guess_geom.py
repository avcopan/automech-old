#!/usr/bin/env python
""" run rc-driver for a single species
"""
import sys
import automol

# read in the command line arguments
assert len(sys.argv) == 3
INCHI = sys.argv[1]
MULT = sys.argv[2]

# do stuff
GEO = automol.inchi.geometry(INCHI)
SMI = automol.inchi.smiles(INCHI)

DXYZ_STR = automol.geom.dxyz_string(GEO)
FILE_NAME = '{:s}.xyz'.format(SMI)
with open(FILE_NAME, 'w') as file_obj:
    file_obj.write(DXYZ_STR)
