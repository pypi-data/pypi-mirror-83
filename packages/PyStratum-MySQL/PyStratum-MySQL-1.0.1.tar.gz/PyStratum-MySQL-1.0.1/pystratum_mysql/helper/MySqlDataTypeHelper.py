from typing import Any, Dict

from pystratum_common.helper.DataTypeHelper import DataTypeHelper


class MySqlDataTypeHelper(DataTypeHelper):
    """
    Utility class for deriving information based on a MySQL data type.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def column_type_to_python_type(self, data_type_info: Dict[str, Any]) -> str:
        """
        Returns the corresponding Python data type of a MySQL data type.

        :param dict data_type_info: The MySQL data type metadata.

        :rtype: str
        """
        if data_type_info['data_type'] in ['tinyint',
                                           'smallint',
                                           'mediumint',
                                           'int',
                                           'bigint',
                                           'year',
                                           'bit']:
            return 'int'

        if data_type_info['data_type'] == 'decimal':
            return 'int' if data_type_info['numeric_scale'] == 0 else 'float'

        if data_type_info['data_type'] in ['float',
                                           'double']:
            return 'float'

        if data_type_info['data_type'] in ['char',
                                           'varchar',
                                           'time',
                                           'timestamp',
                                           'date',
                                           'datetime',
                                           'enum',
                                           'set',
                                           'tinytext',
                                           'text',
                                           'mediumtext',
                                           'longtext']:
            return 'str'

        if data_type_info['data_type'] in ['varbinary',
                                           'binary',
                                           'tinyblob',
                                           'blob',
                                           'mediumblob',
                                           'longblob', ]:
            return 'bytes'

        raise RuntimeError('Unknown data type {0}'.format(data_type_info['data_type']))

    # ------------------------------------------------------------------------------------------------------------------
    def column_type_to_python_type_hint(self, data_type_info: Dict[str, Any]) -> str:
        """
        Returns the corresponding Python data type hinting of a MySQL data type.

        :param dict data_type_info: The MySQL data type metadata.

        :rtype: str
        """
        if data_type_info['data_type'] in ['tinyint',
                                           'smallint',
                                           'mediumint',
                                           'int',
                                           'bigint',
                                           'year',
                                           'bit']:
            return 'Optional[int]'

        if data_type_info['data_type'] == 'decimal':
            return 'Optional[int]' if data_type_info['numeric_scale'] == 0 else 'Optional[float]'

        if data_type_info['data_type'] in ['float',
                                           'double']:
            return 'Optional[float]'

        if data_type_info['data_type'] in ['char',
                                           'varchar',
                                           'time',
                                           'timestamp',
                                           'date',
                                           'datetime',
                                           'enum',
                                           'set',
                                           'tinytext',
                                           'text',
                                           'mediumtext',
                                           'longtext']:
            return 'Optional[str]'

        if data_type_info['data_type'] in ['varbinary',
                                           'binary',
                                           'tinyblob',
                                           'blob',
                                           'mediumblob',
                                           'longblob', ]:
            return 'Optional[bytes]'

        raise RuntimeError('Unknown data type {0}'.format(data_type_info['data_type']))

# ----------------------------------------------------------------------------------------------------------------------
