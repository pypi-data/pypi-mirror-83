from typing import Dict, Optional, Union

from mysql.connector import MySQLConnection

from pystratum_mysql.MySqlConnector import MySqlConnector


class MySqlDefaultConnector(MySqlConnector):
    """
    Connects to a MySQL instance using user name and password.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params: Dict[str, Union[str, int]]):
        """
        Object constructor.
        
        :param params: The connection parameters.
        """

        self._params: Dict[str, Union[str, int]] = params
        """
        The connection parameters.
        """

        self._connection: Optional[MySQLConnection] = None
        """
        The connection between Python and the MySQL instance.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self) -> MySQLConnection:
        """
        Connects to the MySQL instance.
        """
        self._connection = MySQLConnection(**self._params)

        return self._connection

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self) -> None:
        """
        Disconnects from the MySQL instance.
        """
        if self._connection:
            self._connection.disconnect()
            self._connection = None

# ----------------------------------------------------------------------------------------------------------------------
