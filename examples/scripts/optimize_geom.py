#!/usr/bin/env python
""" run rc-driver for a single species
"""
import sys
import subprocess
import automol
import elstruct


# read in the command line arguments
assert len(sys.argv) == 3
INCHI = sys.argv[1]
MULT = sys.argv[2]

# do stuff
PROG = 'psi4'
METHOD = 'uhf-mp2'
BASIS = '6-31g'
GEO = automol.inchi.geometry(INCHI)

if len(GEO) > 1:
    INP_STR = elstruct.write.optimization_input_string(
        prog=PROG, method=METHOD, basis=BASIS, geom=GEO, charge=0,
        mult=MULT,
        scf_options='set scf_type df',
        corr_options='set mp2_type df',
        mol_options='symmetry c1',
    )

    with open('input.dat', 'w') as file_obj:
        file_obj.write(INP_STR)

    subprocess.check_call(['psi4'])
