from typing import Any, Dict

from pystratum_common.wrapper.BulkWrapper import BulkWrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlBulkWrapper(MySqlWrapper, BulkWrapper):
    """
    Wrapper method generator for stored procedures with large result sets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_bulk(bulk_handler, {0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
