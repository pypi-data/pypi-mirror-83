from typing import Dict, Any

from pystratum_common.wrapper.TableWrapper import TableWrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlTableWrapper(MySqlWrapper, TableWrapper):
    """
    Wrapper method generator for printing the result set of stored procedures in a table format.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_table({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
