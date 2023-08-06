from time import gmtime, strftime
from typing import Any, Dict, List, Optional

from mysql.connector import InterfaceError, MySQLConnection
from mysql.connector.cursor import MySQLCursor, MySQLCursorBuffered, MySQLCursorBufferedDict, MySQLCursorDict
from pystratum_middle.BulkHandler import BulkHandler
from pystratum_middle.exception.ResultException import ResultException

from pystratum_mysql.MySqlConnector import MySqlConnector


class MySqlDataLayer:
    """
    Class for connecting to a MySQL instance and executing SQL statements. Also, a parent class for classes with
    static wrapper methods for executing stored procedures and functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, connector: MySqlConnector):
        """
        Object constructor.
        """

        self.__connector: MySqlConnector = connector
        """
        The object for connecting to a MySQL instance.
        """

        self._connection: Optional[MySQLConnection] = None
        """
        The connection between Python and the MySQL instance.
        """

        self.line_buffered: bool = True
        """
        If True log messages from stored procedures with designation type 'log' are line buffered (Note: In python
        sys.stdout is buffered by default).
        """

        self._last_sql: str = ''
        """
        The last executed SQL statement.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def commit(self) -> None:
        """
        Commits the current transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-commit.html
        """
        self._connection.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self) -> None:
        """
        Connects to a MySQL instance. See http://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        for a complete overview of all possible keys in config.
        """
        self._connection = self.__connector.connect()

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self) -> None:
        """
        Disconnects from the MySQL instance.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-disconnect.html.
        """
        self._connection = None
        self.__connector.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_multi(self, sql: str) -> None:
        """
        Executes a multi query that does not select any rows.

        :param str sql: The SQL statements.
        """
        self._last_sql = sql

        cursor = MySQLCursor(self._connection)
        for _ in cursor.execute(sql, multi=True):
            pass
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_none(self, sql: str, *params) -> int:
        """
        Executes a query that does not select any rows. Returns the number of affected rows.

        :param str sql: The SQL statement.
        :param iterable params: The values for the statement.

        :rtype: int
        """
        self._last_sql = sql

        cursor = MySQLCursor(self._connection)
        cursor.execute(sql, params)
        rowcount = cursor.rowcount
        cursor.close()

        return rowcount

    # ------------------------------------------------------------------------------------------------------------------
    def execute_rows(self, sql: str, *params) -> List[Dict[str, Any]]:
        """
        Executes a query that selects 0 or more rows. Returns the selected rows (an empty list if no rows are selected).

        :param str sql: The SQL statement.
        :param iterable params: The arguments for the statement.

        :rtype: list[dict[str,*]]
        """
        self._last_sql = sql

        cursor = MySQLCursorBufferedDict(self._connection)
        cursor.execute(sql, *params)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def execute_singleton1(self, sql: str, *params) -> Any:
        """
        Executes SQL statement that selects 1 row with 1 column. Returns the value of the selected column.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: *:
        """
        self._last_sql = sql

        cursor = MySQLCursorBuffered(self._connection)
        cursor.execute(sql, params)
        rowcount = cursor.rowcount
        if rowcount == 1:
            ret = cursor.fetchone()[0]
        else:
            ret = None  # Keep our IDE happy.
        cursor.close()

        if rowcount != 1:
            raise ResultException('1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_bulk(self, bulk_handler: BulkHandler, sql: str, *params) -> int:
        """
        Executes a stored routine with designation type "bulk". Returns the number of rows processed.

        :param BulkHandler bulk_handler: The bulk handler for processing the selected rows.
        :param str sql: The SQL statement for calling the stored routine.
        :param iterable params: The arguments for calling the stored routine.

        :rtype: int
        """
        self._last_sql = sql

        cursor = MySQLCursorDict(self._connection)
        itr = cursor.execute(sql, params, multi=True)
        bulk_handler.start()

        rowcount = 0
        for result in itr:
            for row in result:
                rowcount += 1
                bulk_handler.row(row)

        cursor.close()
        bulk_handler.stop()

        return rowcount

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_log(self, sql: str, *params) -> int:
        """
        Executes a stored routine with designation type "log". Returns the number of log messages.

        :param str sql: The SQL statement for calling the stored routine.
        :param iterable params: The arguments for calling the stored routine.

        :rtype: int
        """
        self._last_sql = sql

        cursor = MySQLCursorBuffered(self._connection)
        itr = cursor.execute(sql, params, multi=True)

        rowcount = 0
        try:
            for result in itr:
                rows = result.fetchall()
                if rows is not None:
                    stamp = strftime('%Y-%m-%d %H:%M:%S', gmtime())
                    for row in rows:
                        print(stamp, end='')
                        for field in row:
                            print(' %s' % field, end='')
                        print('', flush=self.line_buffered)
                        rowcount += 1
        except InterfaceError:
            pass

        cursor.close()

        return rowcount

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_multi(self, sql: str, *params) -> List[List[Dict[str, Any]]]:
        """
        Executes a stored routine with designation type "multi". Returns a list of the result sets.

        :param str sql: The SQL statement for calling the stored routine.
        :param iterable params: The arguments for calling the stored routine.

        :rtype: list[list[dict[str,*]]]
        """
        self._last_sql = sql

        cursor = MySQLCursorBufferedDict(self._connection)
        itr = cursor.execute(sql, params, multi=True)

        results = []
        try:
            for result in itr:
                results.append(result.fetchall())
        except InterfaceError:
            pass

        cursor.close()

        return results

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_none(self, sql: str, *params) -> int:
        """
        Executes a stored routine that does not select any rows. Returns the number of affected rows.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: int
        """
        self._last_sql = sql

        cursor = MySQLCursor(self._connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        cursor.close()

        return rowcount

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_row0(self, sql: str, *params) -> Optional[Dict[str, Any]]:
        """
        Executes a stored procedure that selects 0 or 1 row. Returns the selected row or None.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: None|dict[str,*]
        """
        self._last_sql = sql

        cursor = MySQLCursorBufferedDict(self._connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()
        else:
            ret = None
        itr.__next__()
        cursor.close()

        if not (rowcount == 0 or rowcount == 1):
            raise ResultException('0 or 1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_row1(self, sql: str, *params) -> Dict[str, Any]:
        """
        Executes a stored procedure that selects 1 row. Returns the selected row.

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: dict[str,*]
        """
        self._last_sql = sql

        cursor = MySQLCursorBufferedDict(self._connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()
        else:
            ret = None  # Keep our IDE happy.
        itr.__next__()
        cursor.close()

        if rowcount != 1:
            raise ResultException('1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_rows(self, sql: str, *params) -> List[Dict[str, Any]]:
        """
        Executes a stored procedure that selects 0 or more rows. Returns the selected rows (an empty list if no rows
        are selected).

        :param str sql: The SQL statement.
        :param iterable params: The arguments for the statement.

        :rtype: list[dict[str,*]]
        """
        self._last_sql = sql

        cursor = MySQLCursorBufferedDict(self._connection)
        itr = cursor.execute(sql, params, multi=True)
        ret = itr.__next__().fetchall()
        itr.__next__()
        cursor.close()

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_singleton0(self, sql: str, *params) -> Any:
        """
        Executes a stored procedure that selects 0 or 1 row with 1 column. Returns the value of selected column or None.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: *
        """
        self._last_sql = sql

        cursor = MySQLCursorBuffered(self._connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()[0]
        else:
            ret = None
        itr.__next__()
        cursor.close()

        if not (rowcount == 0 or rowcount == 1):
            raise ResultException('0 or 1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_singleton1(self, sql: str, *params) -> Any:
        """
        Executes a stored routine with designation type "table", i.e a stored routine that is expected to select 1 row
        with 1 column.

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: * The value of the selected column.
        """
        self._last_sql = sql

        cursor = MySQLCursorBuffered(self._connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()[0]
        else:
            ret = None  # Keep our IDE happy.
        itr.__next__()
        cursor.close()

        if rowcount != 1:
            raise ResultException('1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def last_sql(self) -> str:
        """
        Returns the last execute SQL statement.
        """
        return self._last_sql

    # ------------------------------------------------------------------------------------------------------------------
    def rollback(self) -> None:
        """
        Rolls back the current transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-rollback.html
        """
        self._connection.rollback()

    # ------------------------------------------------------------------------------------------------------------------
    def start_transaction(self,
                          consistent_snapshot: bool = False,
                          isolation_level: str = 'READ-COMMITTED',
                          readonly: Optional[bool] = None) -> None:
        """
        Starts a transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-start-transaction.html

        :param bool consistent_snapshot:
        :param str isolation_level:
        :param bool readonly:
        """
        self._connection.start_transaction(consistent_snapshot, isolation_level, readonly)

# ----------------------------------------------------------------------------------------------------------------------
