from typing import Any, Dict

from pystratum_mysql.wrapper.MySqlBulkWrapper import MySqlBulkWrapper
from pystratum_mysql.wrapper.MySqlFunctionsWrapper import MySqlFunctionsWrapper
from pystratum_mysql.wrapper.MySqlLogWrapper import MySqlLogWrapper
from pystratum_mysql.wrapper.MySqlMultiWrapper import MySqlMultiWrapper
from pystratum_mysql.wrapper.MySqlNoneWrapper import MySqlNoneWrapper
from pystratum_mysql.wrapper.MySqlRow0Wrapper import MySqlRow0Wrapper
from pystratum_mysql.wrapper.MySqlRow1Wrapper import MySqlRow1Wrapper
from pystratum_mysql.wrapper.MySqlRowsWithIndexWrapper import MySqlRowsWithIndexWrapper
from pystratum_mysql.wrapper.MySqlRowsWithKeyWrapper import MySqlRowsWithKeyWrapper
from pystratum_mysql.wrapper.MySqlRowsWrapper import MySqlRowsWrapper
from pystratum_mysql.wrapper.MySqlSingleton0Wrapper import MySqlSingleton0Wrapper
from pystratum_mysql.wrapper.MySqlSingleton1Wrapper import MySqlSingleton1Wrapper


# ----------------------------------------------------------------------------------------------------------------------
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


def create_routine_wrapper(routine: Dict[str, Any], lob_as_string_flag: bool) -> MySqlWrapper:
    """
    A factory for creating the appropriate object for generating a wrapper method for a stored routine.

    :param dict[str,str] routine: The metadata of the sored routine.
    :param bool lob_as_string_flag: If True BLOBs and CLOBs must be treated as strings.

    :rtype: MySqlWrapper
    """
    if routine['designation'] == 'bulk':
        wrapper = MySqlBulkWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'function':
        wrapper = MySqlFunctionsWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'log':
        wrapper = MySqlLogWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'multi':
        wrapper = MySqlMultiWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'none':
        wrapper = MySqlNoneWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'row0':
        wrapper = MySqlRow0Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'row1':
        wrapper = MySqlRow1Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows_with_index':
        wrapper = MySqlRowsWithIndexWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows_with_key':
        wrapper = MySqlRowsWithKeyWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows':
        wrapper = MySqlRowsWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'singleton0':
        wrapper = MySqlSingleton0Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'singleton1':
        wrapper = MySqlSingleton1Wrapper(routine, lob_as_string_flag)
    else:
        raise Exception("Unknown routine type '{0!s}'.".format(routine['designation']))

    return wrapper

# ----------------------------------------------------------------------------------------------------------------------
