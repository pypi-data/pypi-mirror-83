from typing import Dict, Any

from pystratum_common.wrapper.RowsWrapper import RowsWrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlRowsWrapper(MySqlWrapper, RowsWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0, 1, or more rows.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _return_type_hint(self) -> str:
        """
        Returns the return type hint of the wrapper method.

        :rtype: str
        """
        return 'List[Dict[str, Any]]'

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        self._write_line('return self.execute_sp_rows({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
