"""MySQL database operations helper module."""

from typing import Any, Dict, List, Optional, Tuple, Iterator
from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error as MySQLError
from mysql.connector.cursor import MySQLCursor


class MySQLHelper:
    """Helper class for MySQL database operations."""

    def __init__(self, logger: Any, config: Dict[str, Any]) -> None:
        """Initialize MySQL helper with logger and configuration.

        Args:
            logger: Logger instance for logging operations
            config: Configuration dictionary containing MySQL credentials and settings
        """
        self._logger = logger
        self._config = config
        self._connection = None

    @contextmanager
    def _get_connection(self) -> Iterator[mysql.connector.MySQLConnection]:
        """Get a MySQL connection using context manager.

        Yields:
            MySQLConnection: Active database connection

        Raises:
            MySQLError: If connection fails
        """
        try:
            if not self._connection or not self._connection.is_connected():
                self._connection = mysql.connector.connect(
                    host=self._config["database"]["mysql"]["host"],
                    user=self._config["database"]["mysql"]["username"],
                    password=self._config["database"]["mysql"]["password"],
                    database=self._config["database"]["mysql"]["database"],
                    raise_on_warnings=False,
                )
            yield self._connection  # type: ignore
        except MySQLError as e:
            self._logger.exception(f"Failed to connect to MySQL: {str(e)}")
            raise
        finally:
            if self._connection and self._connection.is_connected():
                self._connection.close()

    @contextmanager
    def _get_cursor(self, dictionary: bool = False) -> MySQLCursor:  # type: ignore
        """Get a MySQL cursor using context manager.

        Args:
            dictionary: If True, returns results as dictionaries

        Yields:
            MySQLCursor: Database cursor

        Raises:
            MySQLError: If cursor creation fails
        """
        with self._get_connection() as conn:
            cursor = None
            try:
                cursor = conn.cursor(dictionary=dictionary)
                yield cursor  # type: ignore
            finally:
                if cursor:
                    cursor.close()

    def fetch_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Execute a SELECT query and return results.

        Args:
            query: SQL SELECT query to execute

        Returns:
            List of dictionaries containing query results, or None if query fails
        """
        try:
            with self._get_cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except MySQLError as e:
            self._logger.exception(f"Failed to execute query: {str(e)}")
            return None

    def execute_query(
        self,
        query: str,
        params: Optional[Tuple[Any, ...]] = None,
        *,
        commit: bool = True,
    ) -> Optional[bool]:
        """Execute a query with optional parameters and commit.

        Args:
            query: SQL query to execute
            params: Optional tuple of query parameters
            commit: Whether to commit the transaction

        Returns:
            bool: True if successful, False if error, None if duplicate entry
        """
        try:
            with self._get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if commit:
                    if self._connection:
                        self._connection.commit()
                return True

        except MySQLError as e:
            error_code = str(e).split(":")[0]
            if error_code == "1062 (23000)":
                self._logger.warning("Duplicate entry detected")
                return None

            self._logger.exception(f"MySQL error executing query: {str(e)}")
            self._logger.error(f"Failed query: {query}")
            return False

        except Exception as e:
            self._logger.exception(f"Unexpected error executing query: {str(e)}")
            return False
