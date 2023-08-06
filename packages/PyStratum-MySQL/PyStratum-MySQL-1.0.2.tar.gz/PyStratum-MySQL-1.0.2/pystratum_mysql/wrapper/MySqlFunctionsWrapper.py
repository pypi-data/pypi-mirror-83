from typing import Dict, Any

from pystratum_common.wrapper.FunctionsWrapper import FunctionsWrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlFunctionsWrapper(MySqlWrapper, FunctionsWrapper):
    """
    Wrapper method generator for stored functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_singleton1({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
