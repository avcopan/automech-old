""" automechanic run parameters
"""
import os
from . import tab

# some english names for things
CHK_ENG = 'chemkin'
SPC_ENG = 'species'
RXN_ENG = 'reactions'

PRS_ENG = 'parse'
ICH_ENG = 'inchi'
SMI_ENG = 'smiles'
FLS_ENG = 'filesystem'
MECH_ENG = 'mechanism'

# extensions
CSV_EXT = 'csv'
TXT_EXT = 'txt'

# common schema parameters
_NAME_KEY = 'name'
_NAME_TYP = tab.dt_(str)
_ICH_KEY = ICH_ENG
_ICH_TYP = tab.dt_(str)
_SMI_KEY = SMI_ENG
_SMI_TYP = tab.dt_(str)
_MULT_KEY = 'mult'
_MULT_TYP = tab.dt_(int)
_FILESYSTEM_PATH_KEY = 'path'
_FILESYSTEM_PATH_TYP = tab.dt_(str)
_STRING_PLACEHOLDER = '{:s}'

INP_TAG = 'inp'
OUT_TAG = 'out'

_HOME_DIR = os.path.expanduser("~")


class MECH():
    """ _ """
    class TXT():
        """ _ """
        NAME = '{:s}_{:s}'.format(MECH_ENG, TXT_EXT)
        HELP_MSG = "CHEMKIN mechanism file"


class FILESYS():
    """ _ """
    NAME = FLS_ENG
    CHAR = 'f'
    HELP_MSG = "Path to automech filesystem"
    LOCAL_DEFAULT = "AMFS"
    DEFAULT = os.path.join(_HOME_DIR, LOCAL_DEFAULT)


class SPC():
    """ species parameters
    """
    ENGLISH_NAME = SPC_ENG

    MULT_KEY = _MULT_KEY

    ICH_KEY = _ICH_KEY

    FILESYSTEM_DIR_NAME = 'SPC'

    PICK_STEREO = 'pick'
    EXPAND_STEREO = 'expand'

    class TAB():
        """ species table parameters
        """
        NAME_KEY = _NAME_KEY
        NAME_TYP = _NAME_TYP

        CONN_ID_TYP = tab.dt_(str)

        ICH_KEY = _ICH_KEY
        ICH_TYP = _ICH_TYP
        SMI_KEY = _SMI_KEY
        SMI_TYP = _SMI_TYP

        MULT_KEY = _MULT_KEY
        MULT_TYP = _MULT_TYP

        FILESYSTEM_PATH_KEY = _FILESYSTEM_PATH_KEY
        FILESYSTEM_PATH_TYP = _FILESYSTEM_PATH_TYP

        NASA_C_TYP = tab.dt_(float)
        NASA_C_LO_KEYS = ('nasa_lo_1', 'nasa_lo_2', 'nasa_lo_3', 'nasa_lo_4',
                          'nasa_lo_5', 'nasa_lo_6', 'nasa_lo_7')
        NASA_C_HI_KEYS = ('nasa_hi_1', 'nasa_hi_2', 'nasa_hi_3', 'nasa_hi_4',
                          'nasa_hi_5', 'nasa_hi_6', 'nasa_hi_7')
        NASA_T_TYP = tab.dt_(float)
        NASA_T_KEYS = ('t_lo', 't_hi', 't_c')

    class CONN():
        """ _ """
        class ID():
            """ _ """
            NAME = 'id_typ'
            ICH_KEY = ICH_ENG
            SMI_KEY = SMI_ENG
            KEYS = (ICH_KEY, SMI_KEY)
            HELP_MSG = "Species identifier type"

    class STEREO():
        """ _ """
        class MODE():
            """ _ """
            NAME = 'stereo_mode'
            CHAR = 'm'
            PICK_KEY = 'pick'
            EXPAND_KEY = 'expand'
            KEYS = (PICK_KEY, EXPAND_KEY)

    class CSV():
        """ _ """
        CHAR = 's'
        NAME = '{:s}_{:s}'.format(SPC_ENG, CSV_EXT)
        HELP_MSG = "CSV with species data"

        @staticmethod
        def default_name(keyword=None):
            """ _ """
            _name = ('{:s}.{:s}'.format(SPC_ENG, CSV_EXT)
                     if keyword is None else
                     '{:s}_{:s}.{:s}'.format(SPC_ENG, keyword, CSV_EXT))
            return _name


class RXN():
    """ reaction parameters
    """
    ENGLISH_NAME = RXN_ENG
    CSV_ARG_NAME = '{:s}_{:s}'.format(RXN_ENG, CSV_EXT)

    MULT_KEY = _MULT_KEY

    FILESYSTEM_DIR_NAME = 'RXN'

    class TAB():
        """ species table parameters
        """
        NAME_KEY = _NAME_KEY
        NAME_TYP = _NAME_TYP

        CONN_ID_TYP = tab.dt_(str)

        MULT_TYP = _MULT_TYP

        FILESYSTEM_PATH_KEY = _FILESYSTEM_PATH_KEY
        FILESYSTEM_PATH_TYP = _FILESYSTEM_PATH_TYP

        ARRH_TYP = tab.dt_(float)
        ARRH_KEYS = ('arrh_a', 'arrh_b', 'arrh_e')

    class CSV():
        """ _ """
        CHAR = 'r'
        NAME = '{:s}_{:s}'.format(RXN_ENG, CSV_EXT)
        HELP_MSG = "CSV with reaction data"

        @staticmethod
        def default_name(keyword=None):
            """ _ """
            _name = ('{:s}.{:s}'.format(RXN_ENG, CSV_EXT)
                     if keyword is None else
                     '{:s}_{:s}.{:s}'.format(RXN_ENG, keyword, CSV_EXT))
            return _name
