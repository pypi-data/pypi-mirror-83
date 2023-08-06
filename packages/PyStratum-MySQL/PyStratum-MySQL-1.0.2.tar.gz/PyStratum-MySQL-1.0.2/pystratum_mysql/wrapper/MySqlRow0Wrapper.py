from typing import Dict, Any

from pystratum_common.wrapper.Row0Wrapper import Row0Wrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlRow0Wrapper(MySqlWrapper, Row0Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0 or 1 row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_row0({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
