from typing import Any, Dict

from pystratum_common.wrapper.Row1Wrapper import Row1Wrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlRow1Wrapper(MySqlWrapper, Row1Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_row1({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
