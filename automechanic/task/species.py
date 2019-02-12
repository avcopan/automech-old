""" tasks operating on species
"""
import autocom
import automol as mol
from .. import params as par
from .. import tab
from .. import fslib
from .. import fs
from ._util import read_csv as _read_csv
from ._util import write_csv as _write_csv


def inchi_cli(sysargv, calling_pos):
    """ inchi CLI """
    calling_cmd_name = sysargv[calling_pos]
    first_arg_pos = calling_pos + 1

    arg_vals = autocom.values_with_logger(
        sysargv, first_arg_pos, arg_lst=[
            autocom.arg.required(
                'id_key', par.SPC.CONN.ID.NAME, vals=par.SPC.CONN.ID.KEYS,
                msgs=[par.SPC.CONN.ID.HELP_MSG]
            ),
            autocom.arg.required(
                'spc_csv', par.SPC.CSV.NAME, msgs=[par.SPC.CSV.HELP_MSG],
            ),
            autocom.arg.optional(
                'spc_csv_out', par.SPC.CSV.NAME, par.SPC.CSV.CHAR.upper(),
                default=par.SPC.CSV.default_name(calling_cmd_name),
                tag=par.OUT_TAG
            ),
            autocom.arg.optional(
                'ste_mode', par.SPC.STEREO.MODE.NAME, par.SPC.STEREO.MODE.CHAR,
                default=par.SPC.STEREO.MODE.EXPAND_KEY,
                vals=par.SPC.STEREO.MODE.KEYS,
            )
        ]
    )
    inchi(*arg_vals)


def filesystem_cli(sysargv, calling_pos):
    """ filesystem CLI """
    calling_cmd_name = sysargv[calling_pos]
    first_arg_pos = calling_pos + 1

    arg_vals = autocom.values_with_logger(
        sysargv, first_arg_pos, arg_lst=[
            autocom.arg.required(
                'spc_csv', par.SPC.CSV.NAME, msgs=[par.SPC.CSV.HELP_MSG],
            ),
            autocom.arg.optional(
                'spc_csv_out', par.SPC.CSV.NAME, par.SPC.CSV.CHAR.upper(),
                default=par.SPC.CSV.default_name(calling_cmd_name),
                tag=par.OUT_TAG,
            ),
            autocom.arg.optional(
                'fle_sys', par.FILESYS.NAME, par.FILESYS.CHAR.upper(),
                default=par.FILESYS.LOCAL_DEFAULT, tag=par.OUT_TAG,
            )
        ]
    )
    filesystem(*arg_vals)


def inchi(conn_id_key, spc_csv, spc_csv_out, stereo_mode, logger):
    """ convert species identifiers to InChI
    """
    assert conn_id_key in par.SPC.CONN.ID.KEYS
    assert stereo_mode in par.SPC.STEREO.MODE.KEYS

    tbl = _read_csv(spc_csv, logger)
    tbl = _inchi_table(tbl, conn_id_key, logger)
    tbl = _assign_stereo(tbl, mode=stereo_mode, logger=logger)
    _write_csv(spc_csv_out, tbl, logger)


def filesystem(spc_csv, spc_csv_out, filesystem_prefix, logger):
    """ chart the species filesystem structure
    """

    tbl = _read_csv(spc_csv, logger)
    tbl = _create_filesystem(tbl, fs_root_pth=filesystem_prefix, logger=logger)
    _write_csv(spc_csv_out, tbl, logger)


def _inchi_table(tbl, conn_id_key, logger):
    assert conn_id_key in par.SPC.CONN.ID.KEYS
    ich_key = par.SPC.ICH_KEY
    action = ("Calculating" if conn_id_key == ich_key else "Recalculating")
    logger.info("{:s} '{:s}' from '{:s}'".format(action, ich_key, conn_id_key))

    tbl = tab.enforce_schema(tbl,
                             keys=(conn_id_key,),
                             typs=(par.SPC.TAB.CONN_ID_TYP,))

    conv_ = (mol.inchi.recalculate if conn_id_key == par.SPC.CONN.ID.ICH_KEY
             else mol.smiles.inchi)

    conn_ids = tbl[conn_id_key]
    ichs = list(map(conv_, conn_ids))
    tbl = tbl[[key for key in tab.keys_(tbl) if key != conn_id_key]]
    tbl[par.SPC.TAB.ICH_KEY] = ichs
    return tbl


def _assign_stereo(tbl, mode, logger):
    assert mode in (par.SPC.EXPAND_STEREO, par.SPC.PICK_STEREO)
    logger.info("Assigning stereo in mode '{:s}'".format(mode))

    tbl = (_assign_stereo_by_expanding(tbl) if mode == par.SPC.EXPAND_STEREO
           else _assign_stereo_by_picking(tbl))
    return tbl


def _assign_stereo_by_picking(tbl):
    tbl = tab.enforce_schema(tbl,
                             keys=(par.SPC.TAB.ICH_KEY,),
                             typs=(par.SPC.TAB.ICH_TYP,))
    tbl = tbl.copy()
    # use coordinates to get stereo assignments
    ichs = tbl[par.SPC.TAB.ICH_KEY]
    ichs = list(map(mol.geom.stereo_inchi, map(mol.inchi.geometry, ichs)))
    assert not any(map(mol.inchi.has_unknown_stereo_elements, ichs))
    tbl[par.SPC.TAB.ICH_KEY] = ichs
    return tbl


def _assign_stereo_by_expanding(tbl):
    tbl = tab.enforce_schema(tbl,
                             keys=(par.SPC.TAB.ICH_KEY,),
                             typs=(par.SPC.TAB.ICH_TYP,))

    ichs = tbl[par.SPC.TAB.ICH_KEY]
    ichsts_lst = list(map(mol.inchi.compatible_stereoisomers, ichs))

    idx_save_key = tab.next_index_save_key(tbl)
    tbl = tab.save_index(tbl)

    tbl_idxs = tab.idxs_(tbl)
    vals = [[idx, ichst]
            for idx, ichsts in zip(tbl_idxs, ichsts_lst) for ichst in ichsts]
    ste_tbl = tab.from_records(vals,
                               keys=(idx_save_key, par.SPC.TAB.ICH_KEY),
                               typs=(tab.IDX_TYP, par.SPC.TAB.ICH_TYP))

    keys = [key for key in tab.keys_(tbl) if key != par.SPC.TAB.ICH_KEY]
    tbl = tab.left_join(tbl[keys], ste_tbl, key=idx_save_key)
    return tbl


def _create_filesystem(tbl, fs_root_pth, logger):
    logger.info("Creating filesystem at '{:s}'".format(fs_root_pth))

    id_keys = (par.SPC.TAB.ICH_KEY, par.SPC.TAB.MULT_KEY)
    id_typs = (par.SPC.TAB.ICH_TYP, par.SPC.TAB.MULT_TYP)
    tbl = tab.enforce_schema(tbl, keys=id_keys, typs=id_typs)

    def __create_branch(ich, mult):
        sgms = fslib.species.branch_segments(ich, mult)
        return fs.branch.create(sgms)

    with fs.enter(fs_root_pth):
        pth_tbl = tab.from_starmap(tbl, __create_branch, id_keys,
                                   keys=(par.SPC.TAB.FILESYSTEM_PATH_KEY,),
                                   typs=(par.SPC.TAB.FILESYSTEM_PATH_TYP,))
        tbl = tab.left_join(tbl, pth_tbl)

    return tbl


# used elswhere -- decide if this is the best place
def grouped_identifier_lists(tbl, logger):
    """ species identifier lists, grouped by name
    """
    logger.info("Determining species identifiers, by name")

    keys = (par.SPC.TAB.NAME_KEY, par.SPC.TAB.ICH_KEY, par.SPC.TAB.MULT_KEY)
    typs = (par.SPC.TAB.NAME_TYP, par.SPC.TAB.ICH_TYP, par.SPC.TAB.MULT_TYP)
    tbl = tab.enforce_schema(tbl, keys=keys, typs=typs)

    key1 = par.SPC.TAB.NAME_KEY
    key2 = (par.SPC.TAB.ICH_KEY, par.SPC.TAB.MULT_KEY)
    ids_dct = tab.group_dictionary(tbl, key1, key2)
    return ids_dct
