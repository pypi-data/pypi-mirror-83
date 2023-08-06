import re
from typing import Dict, Optional, Any

from mysql import connector
from pystratum_backend.StratumStyle import StratumStyle

from pystratum_common.exception.LoaderException import LoaderException
from pystratum_common.helper.DataTypeHelper import DataTypeHelper
from pystratum_common.helper.RoutineLoaderHelper import RoutineLoaderHelper
from pystratum_mysql.helper.MySqlDataTypeHelper import MySqlDataTypeHelper
from pystratum_mysql.MySqlMetadataDataLayer import MySqlMetadataDataLayer


class MySqlRoutineLoaderHelper(RoutineLoaderHelper):
    """
    Class for loading a single stored routine into a MySQL instance from a (pseudo) SQL file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 io: StratumStyle,
                 dl: MySqlMetadataDataLayer,
                 routine_filename: str,
                 routine_file_encoding: str,
                 pystratum_old_metadata: Optional[Dict],
                 replace_pairs: Dict[str, Any],
                 rdbms_old_metadata: Optional[Dict],
                 sql_mode: str,
                 character_set: str,
                 collate: str):
        """
        Object constructor.
                                
        :param PyStratumStyle io: The output decorator.
        :param MySqlMetadataDataLayer dl: The metadata layer.
        :param str routine_filename: The filename of the source of the stored routine.
        :param str routine_file_encoding: The encoding of the source file.
        :param dict pystratum_old_metadata: The metadata of the stored routine from PyStratum.
        :param dict[str,str] replace_pairs: A map from placeholders to their actual values.
        :param dict rdbms_old_metadata: The old metadata of the stored routine from MS SQL Server.
        :param str sql_mode: The SQL mode under which the stored routine must be loaded and run.
        :param str character_set: The default character set under which the stored routine must be loaded and run.
        :param str collate: The default collate under which the stored routine must be loaded and run.
        """
        RoutineLoaderHelper.__init__(self,
                                     io,
                                     routine_filename,
                                     routine_file_encoding,
                                     pystratum_old_metadata,
                                     replace_pairs,
                                     rdbms_old_metadata)

        self._character_set: str = character_set
        """
        The default character set under which the stored routine will be loaded and run.
        """

        self._collate: str = collate
        """
        The default collate under which the stored routine will be loaded and run.
        """

        self._sql_mode: str = sql_mode
        """
        The SQL-mode under which the stored routine will be loaded and run.
        """
        
        self._dl: MySqlMetadataDataLayer = dl
        """
        The metadata layer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _get_bulk_insert_table_columns_info(self) -> None:
        """
        Gets the column names and column types of the current table for bulk insert.
        """
        table_is_non_temporary = self._dl.check_table_exists(self._table_name)

        if not table_is_non_temporary:
            self._dl.call_stored_routine(self._routine_name)

        columns = self._dl.describe_table(self._table_name)

        tmp_column_types = []
        tmp_fields = []

        n1 = 0
        for column in columns:
            prog = re.compile('(\\w+)')
            c_type = prog.findall(column['Type'])
            tmp_column_types.append(c_type[0])
            tmp_fields.append(column['Field'])
            n1 += 1

        n2 = len(self._columns)

        if not table_is_non_temporary:
            self._dl.drop_temporary_table(self._table_name)

        if n1 != n2:
            raise LoaderException("Number of fields %d and number of columns %d don't match." % (n1, n2))

        self._columns_types = tmp_column_types
        self._fields = tmp_fields

    # ------------------------------------------------------------------------------------------------------------------
    def _get_data_type_helper(self) -> DataTypeHelper:
        """
        Returns a data type helper object for MySQL.

        :rtype: DataTypeHelper
        """
        return MySqlDataTypeHelper()

    # ------------------------------------------------------------------------------------------------------------------
    def _get_name(self) -> None:
        """
        Extracts the name of the stored routine and the stored routine type (i.e. procedure or function) source.
        """
        prog = re.compile("create\\s+(procedure|function)\\s+([a-zA-Z0-9_]+)")
        matches = prog.findall(self._routine_source_code)

        if matches:
            self._routine_type = matches[0][0].lower()

            if self._routine_name != matches[0][1]:
                raise LoaderException('Stored routine name {0} does not match filename in file {1}'.
                                      format(matches[0][1], self._source_filename))

        if not self._routine_type:
            raise LoaderException('Unable to find the stored routine name and type in file {0}'.
                                  format(self._source_filename))

    # ------------------------------------------------------------------------------------------------------------------
    def _get_routine_parameters_info(self) -> None:
        """
        Retrieves information about the stored routine parameters from the meta data of MySQL.
        """
        routine_parameters = self._dl.get_routine_parameters(self._routine_name)
        for routine_parameter in routine_parameters:
            if routine_parameter['parameter_name']:
                value = routine_parameter['column_type']
                if 'character_set_name' in routine_parameter:
                    if routine_parameter['character_set_name']:
                        value += ' character set %s' % routine_parameter['character_set_name']
                if 'collation' in routine_parameter:
                    if routine_parameter['character_set_name']:
                        value += ' collation %s' % routine_parameter['collation']

                self._parameters.append({'name':                 routine_parameter['parameter_name'],
                                         'data_type':            routine_parameter['parameter_type'],
                                         'numeric_precision':    routine_parameter['numeric_precision'],
                                         'numeric_scale':        routine_parameter['numeric_scale'],
                                         'data_type_descriptor': value})

    # ------------------------------------------------------------------------------------------------------------------
    def _is_start_of_stored_routine(self, line: str) -> bool:
        """
        Returns True if a line is the start of the code of the stored routine.

        :param str line: The line with source code of the stored routine.

        :rtype: bool
        """
        return re.match(r'^\s*create\s+(procedure|function)', line, re.IGNORECASE) is not None

    # ------------------------------------------------------------------------------------------------------------------
    def _is_start_of_stored_routine_body(self, line: str) -> bool:
        """
        Returns True if a line is the start of the body of the stored routine.

        :param str line: The line with source code of the stored routine.

        :rtype: bool
        """
        return re.match(r'^\s*begin', line, re.IGNORECASE) is not None

    # ------------------------------------------------------------------------------------------------------------------
    def _load_routine_file(self) -> None:
        """
        Loads the stored routine into the MySQL instance.
        """
        self._io.text('Loading {0} <dbo>{1}</dbo>'.format(self._routine_type, self._routine_name))

        self._unset_magic_constants()
        self._drop_routine()

        self._dl.set_sql_mode(self._sql_mode)

        self._dl.set_character_set(self._character_set, self._collate)

        self._dl.execute_none(self._routine_source_code)

    # ------------------------------------------------------------------------------------------------------------------
    def _log_exception(self, exception: Exception) -> None:
        """
        Logs an exception.

        :param Exception exception: The exception.
        """
        RoutineLoaderHelper._log_exception(self, exception)

        if isinstance(exception, connector.errors.Error):
            if exception.errno == 1064:
                # Exception is caused by an invalid SQL statement.
                sql = self._dl.last_sql()
                if sql:
                    sql = sql.strip()
                    # The format of a 1064 message is: %s near '%s' at line %d
                    parts = re.search(r'(\d+)$', exception.msg)
                    if parts:
                        error_line = int(parts.group(1))
                    else:
                        error_line = 0

                    self._print_sql_with_error(sql, error_line)

    # ------------------------------------------------------------------------------------------------------------------
    def _must_reload(self) -> bool:
        """
        Returns True if the source file must be load or reloaded. Otherwise returns False.

        :rtype: bool
        """
        if not self._pystratum_old_metadata:
            return True

        if self._pystratum_old_metadata['timestamp'] != self._m_time:
            return True

        if self._pystratum_old_metadata['replace']:
            for key, value in self._pystratum_old_metadata['replace'].items():
                if key.lower() not in self._replace_pairs or self._replace_pairs[key.lower()] != value:
                    return True

        if not self._rdbms_old_metadata:
            return True

        if self._rdbms_old_metadata['sql_mode'] != self._sql_mode:
            return True

        if self._rdbms_old_metadata['character_set_client'] != self._character_set:
            return True

        if self._rdbms_old_metadata['collation_connection'] != self._collate:
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_routine(self) -> None:
        """
        Drops the stored routine if it exists.
        """
        if self._rdbms_old_metadata:
            self._dl.drop_stored_routine(self._rdbms_old_metadata['routine_type'], self._routine_name)

# ----------------------------------------------------------------------------------------------------------------------
