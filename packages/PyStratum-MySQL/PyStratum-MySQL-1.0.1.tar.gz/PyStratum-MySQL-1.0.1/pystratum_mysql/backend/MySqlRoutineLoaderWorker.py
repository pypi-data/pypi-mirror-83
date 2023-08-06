from configparser import ConfigParser
from typing import Any, Dict, List, Optional

from pystratum_backend.StratumStyle import StratumStyle

from pystratum_common.backend.CommonRoutineLoaderWorker import CommonRoutineLoaderWorker
from pystratum_mysql.backend.MySqlWorker import MySqlWorker
from pystratum_mysql.helper.MySqlRoutineLoaderHelper import MySqlRoutineLoaderHelper


class MySqlRoutineLoaderWorker(MySqlWorker, CommonRoutineLoaderWorker):
    """
    Class for loading stored routines into a MySQL instance from (pseudo) SQL files.
    """
    MAX_LENGTH_CHAR = 255
    """
    Maximum length of a varchar.
    """

    MAX_LENGTH_VARCHAR = 4096
    """
    Maximum length of a varchar.
    """

    MAX_LENGTH_BINARY = 255
    """
    Maximum length of a varbinary.
    """

    MAX_LENGTH_VARBINARY = 4096
    """
    Maximum length of a varbinary.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle, config: ConfigParser):
        """
        Object constructor.

        :param PyStratumStyle io: The output decorator.
        """
        MySqlWorker.__init__(self, io, config)
        CommonRoutineLoaderWorker.__init__(self, io, config)

        self._character_set_client: Optional[str] = None
        """
        The default character set under which the stored routine will be loaded and run.
        """

        self._collation_connection: Optional[str] = None
        """
        The default collate under which the stored routine will be loaded and run.
        """

        self._sql_mode: Optional[str] = None
        """
        
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __save_column_types_exact(self, rows: List[Dict[str, Any]]) -> None:
        """
        Saves the exact column types as replace pairs.

        :param list[dict[str,*]] rows: The columns types.
        """
        for row in rows:
            key = row['table_name'] + '.' + row['column_name'] + '%type'

            value = row['column_type']
            if row['character_set_name']:
                value += ' character set ' + row['character_set_name']

            self._add_replace_pair(key, value, False)

    # ------------------------------------------------------------------------------------------------------------------
    def __save_column_types_max_length(self, rows: List[Dict[str, Any]]) -> None:
        """
        Saves the column types with maximum length as replace pairs.

        :param list[dict[str,*]] rows: The columns types.
        """
        for row in rows:
            key = row['table_name'] + '.' + row['column_name'] + '%max-type'

            if row['data_type'] == 'char':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_CHAR) + ')'
                value += ' character set ' + row['character_set_name']
                self._add_replace_pair(key, value, False)

            if row['data_type'] == 'varchar':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_VARCHAR) + ')'
                value += ' character set ' + row['character_set_name']
                self._add_replace_pair(key, value, False)

            elif row['data_type'] == 'binary':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_BINARY) + ')'
                self._add_replace_pair(key, value, False)

            elif row['data_type'] == 'varbinary':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_VARBINARY) + ')'
                self._add_replace_pair(key, value, False)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self) -> None:
        """
        Selects schema, table, column names and the column type from MySQL and saves them as replace pairs.
        """
        rows = self._dl.get_all_table_columns()
        self.__save_column_types_exact(rows)
        self.__save_column_types_max_length(rows)

        self._io.text('Selected {0} column types for substitution'.format(len(rows)))

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_helper(self,
                                     routine_name: str,
                                     pystratum_old_metadata: Optional[Dict],
                                     rdbms_old_metadata: Optional[Dict]) -> MySqlRoutineLoaderHelper:
        """
        Creates a Routine Loader Helper object.

        :param str routine_name: The name of the routine.
        :param dict pystratum_old_metadata: The old metadata of the stored routine from PyStratum.
        :param dict rdbms_old_metadata:  The old metadata of the stored routine from MySQL.

        :rtype: MySqlRoutineLoaderHelper
        """
        return MySqlRoutineLoaderHelper(self._io,
                                        self._dl,
                                        self._source_file_names[routine_name],
                                        self._source_file_encoding,
                                        pystratum_old_metadata,
                                        self._replace_pairs,
                                        rdbms_old_metadata,
                                        self._sql_mode,
                                        self._character_set_client,
                                        self._collation_connection)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_stored_routine_info(self) -> None:
        """
        Retrieves information about all stored routines in the current schema.
        """
        rows = self._dl.get_routines()
        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['routine_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _get_correct_sql_mode(self) -> None:
        """
        Gets the SQL mode in the order as preferred by MySQL.
        """
        self._sql_mode = self._dl.get_correct_sql_mode(self._sql_mode)

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self) -> None:
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        for routine_name, values in self._rdbms_old_metadata.items():
            if routine_name not in self._source_file_names:
                self._io.writeln("Dropping {0} <dbo>{1}</dbo>".format(values['routine_type'].lower(), routine_name))
                self._dl.drop_stored_routine(values['routine_type'], routine_name)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self) -> None:
        """
        Reads parameters from the configuration file.
        """
        CommonRoutineLoaderWorker._read_configuration_file(self)

        self._character_set_client = self._config.get('database', 'character_set_client', fallback='utf-8')
        self._collation_connection = self._config.get('database', 'collation_connection', fallback='utf8_general_ci')
        self._sql_mode = self._config.get('database', 'sql_mode')

# ----------------------------------------------------------------------------------------------------------------------
