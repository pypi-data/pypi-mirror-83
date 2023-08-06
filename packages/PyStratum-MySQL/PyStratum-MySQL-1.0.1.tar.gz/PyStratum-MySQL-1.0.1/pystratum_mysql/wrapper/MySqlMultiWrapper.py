from typing import Dict, Any

from pystratum_common.wrapper.MultiWrapper import MultiWrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlMultiWrapper(MySqlWrapper, MultiWrapper):
    """
    Wrapper method generator for stored procedures with designation type multi.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_multi({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
