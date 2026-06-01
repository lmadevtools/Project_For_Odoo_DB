import unittest
from unittest.mock import patch, MagicMock, call
from Utils.db_connector import DBConnector
from Utils import queries


class TestDBConnectorInit(unittest.TestCase):

    def test_init_connection_none(self):
        db = DBConnector()
        self.assertIsNone(db._connection)
        self.assertIsNone(db._cursor)

#using @patch to works with mock (fake object to avoir connecting to the true DB)
class TestDBConnectorConnect(unittest.TestCase):

    @patch("Utils.db_connector.psycopg2.connect")
    def test_connect_initializes_connection(self, mock_connect):
        mock_conn   = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value     = mock_conn

        db = DBConnector()
        db.connect()

        self.assertEqual(db._connection, mock_conn)
        self.assertEqual(db._cursor,     mock_cursor)

    @patch("Utils.db_connector.psycopg2.connect")
    def test_connect_calls_psycopg2_with_config(self, mock_connect):
        mock_connect.return_value = MagicMock()
        mock_connect.return_value.cursor.return_value = MagicMock()

        db = DBConnector()
        db.connect()

        mock_connect.assert_called_once()

    @patch("Utils.db_connector.psycopg2.connect", side_effect=Exception("Connection failed"))
    def test_connect_handles_exception(self, mock_connect):
        db = DBConnector()
        # should not raise — exception is caught internally
        try:
            db.connect()
        except Exception:
            self.fail("connect() raised an exception instead of handling it")


class TestDBConnectorDisconnect(unittest.TestCase):

    @patch("Utils.db_connector.psycopg2.connect")
    def test_disconnect_closes_cursor_and_connection(self, mock_connect):
        mock_conn   = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value     = mock_conn

        db = DBConnector()
        db.connect()
        db.disconnect()

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_disconnect_without_connect_does_not_raise(self):
        db = DBConnector()
        try:
            db.disconnect()
        except Exception:
            self.fail("disconnect() raised an exception when not connected")


class TestDBConnectorExecute(unittest.TestCase):

    @patch("Utils.db_connector.psycopg2.connect")
    def test_execute_calls_cursor_execute(self, mock_connect):
        mock_conn   = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value     = mock_conn

        db = DBConnector()
        db.connect()
        db.execute("SELECT * FROM products")

        mock_cursor.execute.assert_called_once_with("SELECT * FROM products", None)

    @patch("Utils.db_connector.psycopg2.connect")
    def test_execute_with_params(self, mock_connect):
        mock_conn   = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value     = mock_conn

        db = DBConnector()
        db.connect()
        db.execute("SELECT * FROM products WHERE product_id = %s", ("P1",))

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM products WHERE product_id = %s", ("P1",)
        )

    @patch("Utils.db_connector.psycopg2.connect")
    def test_execute_returns_cursor(self, mock_connect):
        mock_conn   = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value     = mock_conn

        db     = DBConnector()
        db.connect()
        result = db.execute("SELECT 1")

        self.assertEqual(result, mock_cursor)


class TestDBConnectorCommit(unittest.TestCase):

    @patch("Utils.db_connector.psycopg2.connect")
    def test_commit_calls_connection_commit(self, mock_connect):
        mock_conn   = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value     = mock_conn

        db = DBConnector()
        db.connect()
        db.commit()

        mock_conn.commit.assert_called_once()


# Queries
class TestQueries(unittest.TestCase):

    def test_all_queries_are_strings(self):
        query_names = [
            "CREATE_PRODUCT", "GET_PRODUCT", "LIST_PRODUCTS",
            "UPDATE_PRODUCT", "ARCHIVE_PRODUCT", "UNARCHIVE_PRODUCT",
            "CREATE_CUSTOMER", "GET_CUSTOMER", "LIST_CUSTOMERS",
            "ARCHIVE_CUSTOMER", "UNARCHIVE_CUSTOMER",
            "CREATE_ORDER", "GET_ORDER", "UPDATE_ORDER", "LIST_ORDERS",
            "ADD_ORDER_LINES", "LIST_ORDER_LINES",
            "INSERT_STOCK_MOVES", "LIST_STOCK_MOVES"
        ]
        for name in query_names:
            with self.subTest(query=name):
                self.assertIsInstance(getattr(queries, name), str)

    def test_insert_queries_have_placeholders(self):
        insert_queries = [
            queries.CREATE_PRODUCT,
            queries.CREATE_CUSTOMER,
            queries.CREATE_ORDER,
            queries.ADD_ORDER_LINES,
            queries.INSERT_STOCK_MOVES
        ]
        for q in insert_queries:
            with self.subTest(query=q[:40]):
                self.assertIn("%s", q)

    def test_select_queries_contain_from(self):
        select_queries = [
            queries.GET_PRODUCT,
            queries.LIST_PRODUCTS,
            queries.GET_CUSTOMER,
            queries.LIST_CUSTOMERS,
            queries.GET_ORDER,
            queries.LIST_ORDERS,
            queries.LIST_ORDER_LINES,
            queries.LIST_STOCK_MOVES
        ]
        for q in select_queries:
            with self.subTest(query=q[:40]):
                self.assertIn("FROM", q.upper())

    def test_update_queries_contain_where(self):
        update_queries = [
            queries.UPDATE_PRODUCT,
            queries.ARCHIVE_PRODUCT,
            queries.UNARCHIVE_PRODUCT,
            queries.UPDATE_ORDER,
            queries.ARCHIVE_CUSTOMER,
            queries.UNARCHIVE_CUSTOMER
        ]
        for q in update_queries:
            with self.subTest(query=q[:40]):
                self.assertIn("WHERE", q.upper())

    def test_no_semicolon_in_values(self):
        all_queries = [
            queries.CREATE_PRODUCT, queries.CREATE_CUSTOMER,
            queries.CREATE_ORDER,   queries.ADD_ORDER_LINES,
            queries.INSERT_STOCK_MOVES
        ]
        for q in all_queries:
            with self.subTest(query=q[:40]):
                # extract the VALUES(...) part and check no semicolon inside
                if "VALUES" in q.upper():
                    values_part = q[q.upper().index("VALUES"):]
                    self.assertNotIn(";", values_part)


if __name__ == "__main__":
    unittest.main()
