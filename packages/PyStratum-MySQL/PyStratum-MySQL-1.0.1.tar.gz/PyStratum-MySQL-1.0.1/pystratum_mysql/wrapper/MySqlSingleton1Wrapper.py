from typing import Dict, Any

from pystratum_common.wrapper.Singleton1Wrapper import Singleton1Wrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlSingleton1Wrapper(Singleton1Wrapper, MySqlWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row with one column only.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line(
            'return self.execute_sp_singleton1({0!s})'.format(str(self._generate_command(routine))))

# ----------------------------------------------------------------------------------------------------------------------
