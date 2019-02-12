""" command-line interface for automechanic
"""
import autocom
from . import task


def main(sysargv):
    """ main function """
    return automech(sysargv, calling_pos=0)


def automech(sysargv, calling_pos):
    """ automech main function
    """
    autocom.call_subcommand(
        sysargv, calling_pos, subcmd_func_dct={
            'chemkin': chemkin,
            'species': species,
            'reactions': reactions,
        }
    )


def chemkin(sysargv, calling_pos):
    """ _ """
    autocom.call_subcommand(
        sysargv, calling_pos, subcmd_func_dct={
            'parse': task.chemkin.parse_cli,
        }
    )


def species(sysargv, calling_pos):
    """ _ """
    autocom.call_subcommand(
        sysargv, calling_pos, subcmd_func_dct={
            'inchi': task.species.inchi_cli,
            'filesystem': task.species.filesystem_cli,
        }
    )


def reactions(sysargv, calling_pos):
    """ _ """
    autocom.call_subcommand(
        sysargv, calling_pos, subcmd_func_dct={
            'classify': task.reactions.classify_cli,
        }
    )
