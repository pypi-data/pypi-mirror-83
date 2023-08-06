from typing import Any, Dict, List, Union

from pystratum_backend.StratumStyle import StratumStyle
from pystratum_common.MetadataDataLayer import MetadataDataLayer

from pystratum_mysql.MySqlConnector import MySqlConnector
from pystratum_mysql.MySqlDataLayer import MySqlDataLayer


class MySqlMetadataDataLayer(MetadataDataLayer):
    """
    Data layer for retrieving metadata and loading stored routines.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle, connector: MySqlConnector):
        """
        Object constructor.

        :param PyStratumStyle io: The output decorator.
        """
        super().__init__(io)

        self.__dl: MySqlDataLayer = MySqlDataLayer(connector)
        """
        The connection to the MySQL instance.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def call_stored_routine(self, routine_name: str) -> int:
        """
        Class a stored procedure without arguments.

        :param str routine_name: The name of the procedure.

        :rtype: int
        """
        sql = 'call {0}()'.format(routine_name)

        return self.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def check_table_exists(self, table_name: str) -> int:
        """
        Checks if a table exists in the current schema.

        :param str table_name: The name of the table.

        :rtype: int
        """
        sql = """
select 1 from
information_schema.TABLES
where TABLE_SCHEMA = database()
and   TABLE_NAME   = '{0}'""".format(table_name)

        return self.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self) -> None:
        """
        Connects to a MySQL instance.
        """
        self.__dl.connect()

    # ------------------------------------------------------------------------------------------------------------------
    def describe_table(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Describes a table.

        :param str table_name: The name of the table.

        :rtype: list[dict[str,*]]
        """
        sql = 'describe `{0}`'.format(table_name)

        return self.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self) -> None:
        """
        Disconnects from the MySQL instance.
        """
        self.__dl.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def drop_stored_routine(self, routine_type: str, routine_name: str) -> None:
        """
        Drops a stored routine if it exists.

        :param str routine_type: The type of the routine (i.e. PROCEDURE or FUNCTION).
        :param str routine_name: The name of the routine.
        """
        sql = 'drop {0} if exists `{1}`'.format(routine_type, routine_name)

        self.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def drop_temporary_table(self, table_name: str) -> None:
        """
        Drops a temporary table.

        :param str table_name: The name of the table.
        """
        sql = 'drop temporary table `{0}`'.format(table_name)

        self.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def execute_none(self, query: str) -> int:
        """
        Executes a query that does not select any rows.

        :param str query: The query.

        :rtype: int
        """
        self._log_query(query)

        return self.__dl.execute_none(query)

    # ------------------------------------------------------------------------------------------------------------------
    def execute_rows(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a query that selects 0 or more rows. Returns the selected rows (an empty list if no rows are selected).

        :param str query: The query.

        :rtype: list[dict[str,*]]
        """
        self._log_query(query)

        return self.__dl.execute_rows(query)

    # ------------------------------------------------------------------------------------------------------------------
    def execute_singleton1(self, query: str) -> Any:
        """
        Executes SQL statement that selects 1 row with 1 column. Returns the value of the selected column.

        :param str query: The query.

        :rtype: *
        """
        self._log_query(query)

        return self.__dl.execute_singleton1(query)

    # ------------------------------------------------------------------------------------------------------------------
    def get_all_table_columns(self) -> List[Dict[str, Union[str, int, None]]]:
        """
        Selects metadata of all columns of all tables.

        :rtype: list[dict[str,*]]
        """
        sql = """
(
  select table_name
  ,      column_name
  ,      column_type
  ,      character_set_name
  ,      data_type
  ,      character_maximum_length
  ,      numeric_precision
  ,      ordinal_position
  from   information_schema.COLUMNS
  where  table_schema = database()
  and    table_name  rlike '^[a-zA-Z0-9_]*$'
  and    column_name rlike '^[a-zA-Z0-9_]*$'
  order by table_name
  ,        ordinal_position
)

union all

(
  select concat(table_schema,'.',table_name) table_name
  ,      column_name
  ,      column_type
  ,      character_set_name
  ,      data_type
  ,      character_maximum_length
  ,      numeric_precision
  ,      ordinal_position
  from   information_schema.COLUMNS
  where  table_name  rlike '^[a-zA-Z0-9_]*$'
  and    column_name rlike '^[a-zA-Z0-9_]*$'
  order by table_schema
  ,        table_name
  ,        ordinal_position
)
"""

        return self.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def get_correct_sql_mode(self, sql_mode: str) -> str:
        """
        Selects the SQL mode in the order as preferred by MySQL.

        :param str sql_mode: The SQL mode.

        :rtype: str
        """
        self.set_sql_mode(sql_mode)

        sql = 'select @@sql_mode'

        return self.execute_singleton1(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def get_label_tables(self, regex: str) -> List[Dict[str, Any]]:
        """
        Selects metadata of tables with a label column.

        :param str regex: The regular expression for columns which we want to use.

        :rtype: list[dict[str,*]]
        """
        sql = """
select t1.TABLE_NAME  table_name
,      t1.COLUMN_NAME id
,      t2.COLUMN_NAME label
from       information_schema.COLUMNS t1
inner join information_schema.COLUMNS t2 on t1.TABLE_NAME = t2.TABLE_NAME
where t1.TABLE_SCHEMA = database()
and   t1.EXTRA        = 'auto_increment'
and   t2.TABLE_SCHEMA = database()
and   t2.COLUMN_NAME rlike '{0}'""".format(regex)

        return self.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def get_labels_from_table(self, table_name: str, id_column_name: str, label_column_name: str) -> \
            List[Dict[str, Any]]:
        """
        Selects all labels from a table with labels.

        :param str table_name: The name of the table.
        :param str id_column_name: The name of the auto increment column.
        :param str label_column_name: The name of the column with labels.

        :rtype: list[dict[str,*]]
        """
        sql = """
select `{0}`  as `id`
,      `{1}`  as `label`
from   `{2}`
where   nullif(`{1}`,'') is not null""".format(id_column_name,
                                               label_column_name,
                                               table_name)

        return self.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def last_sql(self) -> str:
        """
        The last executed SQL statement.

        :rtype: str
        """
        return self.__dl.last_sql()

    # ------------------------------------------------------------------------------------------------------------------
    def get_routine_parameters(self, routine_name: str) -> List[Dict[str, Any]]:
        """
        Selects metadata of the parameters of a stored routine.

        :param str routine_name: The name of the routine.

        :rtype: list[dict[str,*]]
        """
        sql = """
select t2.PARAMETER_NAME      parameter_name
,      t2.DATA_TYPE           parameter_type
,      t2.NUMERIC_PRECISION   numeric_precision
,      t2.NUMERIC_SCALE       numeric_scale
,      t2.DTD_IDENTIFIER      column_type
,      t2.CHARACTER_SET_NAME  character_set_name
,      t2.COLLATION_NAME      collation
from            information_schema.ROUTINES   t1
left outer join information_schema.PARAMETERS t2  on  t2.SPECIFIC_SCHEMA = t1.ROUTINE_SCHEMA and
                                                      t2.SPECIFIC_NAME   = t1.ROUTINE_NAME and
                                                      t2.PARAMETER_MODE   is not null
where t1.ROUTINE_SCHEMA = database()
and   t1.ROUTINE_NAME   = '{0}'""".format(routine_name)

        return self.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def get_routines(self) -> List[Dict[str, Any]]:
        """
        Selects metadata of all routines in the current schema.

        :rtype: list[dict[str,*]]
        """
        sql = """
select ROUTINE_NAME           as routine_name
,      ROUTINE_TYPE           as routine_type
,      SQL_MODE               as sql_mode
,      CHARACTER_SET_CLIENT   as character_set_client
,      COLLATION_CONNECTION   as collation_connection
from  information_schema.ROUTINES
where ROUTINE_SCHEMA = database()
order by routine_name"""

        return self.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def set_character_set(self, character_set: str, collate: str) -> None:
        """
        Sets the default character set and collate.

        :param str character_set: The name of the character set.
        :param str collate: The name of the collate
        """
        sql = "set names '{0}' collate '{1}'".format(character_set, collate)

        self.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def set_sql_mode(self, sql_mode: str) -> None:
        """
        Sets the SQL mode.

        :param str sql_mode: The SQL mode.
        """
        sql = "set sql_mode = '{0}'".format(sql_mode)

        self.execute_none(sql)

# ----------------------------------------------------------------------------------------------------------------------
