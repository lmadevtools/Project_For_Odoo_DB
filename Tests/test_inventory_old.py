import unittest
import os
import json
import tempfile
from unittest.mock import patch
from Classes.inventory import Inventory


class TestInventorySetup(unittest.TestCase):

    def setUp(self):
        # temp dir to isolate each test
        self.tmpdir = tempfile.mkdtemp()

        # patch DIR_DATA_FILES to write in temp dir
        self.patcher = patch("Classes.inventory.DIR_DATA_FILES", self.tmpdir + "/")
        self.patcher.start()

        self.inv = Inventory(
            filepathP  = "data_products.json",
            filepathC  = "data_customers.json",
            filepathO  = "data_orders.json",
            filepathSM = "data_stock_moves.json"
        )

    def tearDown(self):
        self.patcher.stop()
        for f in os.listdir(self.tmpdir):
            os.unlink(os.path.join(self.tmpdir, f))
        os.rmdir(self.tmpdir)


######PRODUCTS#######
class TestInventoryProducts(TestInventorySetup):

    def test_add_product(self):
        p = self.inv.add_product("Laptop", 999.99, 10)
        self.assertIn(p.product_id, self.inv.products)
        self.assertEqual(p.name, "Laptop")

    def test_add_product_ids_uniques(self):
        p1 = self.inv.add_product("Laptop", 999.99, 10)
        p2 = self.inv.add_product("Souris", 29.99,  50)
        self.assertNotEqual(p1.product_id, p2.product_id)

    def test_get_product(self):
        p = self.inv.add_product("Laptop", 999.99, 10)
        self.assertEqual(self.inv.get_product(p.product_id).name, "Laptop")

    def test_get_product_unknown_raise_error(self):
        with self.assertRaises(KeyError):
            self.inv.get_product("UNKNOWN")

    def test_list_products_exclude_archives(self):
        p = self.inv.add_product("Laptop", 999.99, 10)
        self.inv.archive_product(p.product_id)
        self.assertEqual(len(self.inv.list_products()), 0)

    def test_list_products_include_archives_if_asked(self):
        p = self.inv.add_product("Laptop", 999.99, 10)
        self.inv.archive_product(p.product_id)
        self.assertEqual(len(self.inv.list_products(include_archived=True)), 1)

    def test_list_low_stock(self):
        self.inv.add_product("Laptop", 999.99, 10, minimum_stock=5)  # ok
        self.inv.add_product("Souris", 29.99,   3, minimum_stock=5)  # bas
        low = self.inv.list_low_stock()
        self.assertEqual(len(low), 1)
        self.assertEqual(low[0].name, "Souris")

    def test_archive_product(self):
        p = self.inv.add_product("Laptop", 999.99, 10)
        self.inv.archive_product(p.product_id)
        self.assertFalse(self.inv.get_product(p.product_id).active)


######CUSTOMERS#######
class TestInventoryCustomers(TestInventorySetup):

    def test_add_customer(self):
        c = self.inv.add_customer("Alice", "alice@example.com")
        self.assertIn(c.customer_id, self.inv.customers)

    def test_get_customer(self):
        c = self.inv.add_customer("Alice", "alice@example.com")
        self.assertEqual(self.inv.get_customer(c.customer_id).name, "Alice")

    def test_get_customer_unknown_raise_error(self):
        with self.assertRaises(KeyError):
            self.inv.get_customer("UNKNOWN")

    def test_list_customers_exclude_archives(self):
        c = self.inv.add_customer("Alice", "alice@example.com")
        c.archive()
        self.assertEqual(len(self.inv.list_customers()), 0)

    def test_list_customers_include_archives_if_asked(self):
        c = self.inv.add_customer("Alice", "alice@example.com")
        c.archive()
        self.assertEqual(len(self.inv.list_customers(include_archived=True)), 1)


######ORDERS#######
class TestInventoryOrders(TestInventorySetup):

    def setUp(self):
        super().setUp()
        self.product  = self.inv.add_product("Laptop", 999.99, 10)
        self.customer = self.inv.add_customer("Alice", "alice@example.com")

    def test_create_order(self):
        o = self.inv.create_order(self.customer.customer_id)
        self.assertIn(o.order_id, self.inv.orders)
        self.assertEqual(o.status, "draft")

    def test_create_order_format_odoo(self):
        o = self.inv.create_order(self.customer.customer_id)
        parts = o.order_id.split("/")
        self.assertEqual(len(parts), 3)
        self.assertTrue(parts[2].isdigit())

    def test_create_order_unknown_customer_raise_error(self):
        with self.assertRaises(KeyError):
            self.inv.create_order("UNKNOWN")

    def test_get_order_unknown_raise_error(self):
        with self.assertRaises(KeyError):
            self.inv.get_order("UNKNOWN")

    def test_confirm_order(self):
        o = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 3)
        self.inv.confirm_order(o.order_id)
        self.assertEqual(o.status, "confirmed")
        self.assertEqual(self.product.quantity, 7)

    def test_confirm_order_traces_stock_moves(self):
        # confirm must create one "out" StockMove per line
        o = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 3)
        self.inv.confirm_order(o.order_id)
        self.assertEqual(len(self.inv.stock_moves), 1)
        self.assertEqual(self.inv.stock_moves[0].direction, "out")
        self.assertEqual(self.inv.stock_moves[0].quantity,  3)
        self.assertIn(o.order_id, self.inv.stock_moves[0].reason)

    def test_confirm_order_multiple_lines_traces_all_moves(self):
        # one StockMove per line
        p2 = self.inv.add_product("Souris", 29.99, 20)
        o  = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 2)
        o.add_line(self.inv.get_product(p2.product_id), 5)
        self.inv.confirm_order(o.order_id)
        self.assertEqual(len(self.inv.stock_moves), 2)
        self.assertTrue(all(m.direction == "out" for m in self.inv.stock_moves))

    def test_cancel_order_from_draft(self):
        o = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 3)
        self.inv.cancel_order(o.order_id)
        self.assertEqual(o.status, "cancelled")

    def test_cancel_order_from_draft_no_stock_move(self):
        # cancelling a draft order must NOT create any StockMove
        o = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 3)
        self.inv.cancel_order(o.order_id)
        self.assertEqual(len(self.inv.stock_moves), 0)

    def test_cancel_order_confirmed_restitue_stock(self):
        o = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 3)
        self.inv.confirm_order(o.order_id)
        self.inv.cancel_order(o.order_id)
        self.assertEqual(self.product.quantity, 10)

    def test_cancel_order_confirmed_traces_stock_moves(self):
        # cancelling a confirmed order must create one "in" StockMove per line
        o = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 3)
        self.inv.confirm_order(o.order_id)
        moves_before = len(self.inv.stock_moves)
        self.inv.cancel_order(o.order_id)
        new_moves = self.inv.stock_moves[moves_before:]
        self.assertEqual(len(new_moves), 1)
        self.assertEqual(new_moves[0].direction, "in")
        self.assertEqual(new_moves[0].quantity,  3)
        self.assertIn(o.order_id, new_moves[0].reason)

    def test_mark_order_done(self):
        o = self.inv.create_order(self.customer.customer_id)
        o.add_line(self.inv.get_product(self.product.product_id), 1)
        self.inv.confirm_order(o.order_id)
        self.inv.mark_order_done(o.order_id)
        self.assertEqual(o.status, "done")

    def test_list_orders_filter_status(self):
        o1 = self.inv.create_order(self.customer.customer_id)
        o2 = self.inv.create_order(self.customer.customer_id)
        o1.add_line(self.inv.get_product(self.product.product_id), 1)
        self.inv.confirm_order(o1.order_id)
        self.assertEqual(len(self.inv.list_orders(status="confirmed")), 1)
        self.assertEqual(len(self.inv.list_orders(status="draft")),     1)


######STOCK MOVES#######
class TestInventoryStockMoves(TestInventorySetup):

    def setUp(self):
        super().setUp()
        self.product = self.inv.add_product("Laptop", 999.99, 10)

    def test_export_csv(self):
        self.inv.add_stock_to_product(self.product.product_id, 5)
        self.inv.export_csv("test_export.csv")
        csv_path = self.tmpdir + "/test_export.csv"
        self.assertTrue(os.path.exists(csv_path))
        with open(csv_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("product_id", content)
        self.assertIn("Laptop",     content)

    def test_export_csv_empty_no_file_creation(self):
        self.inv.export_csv("vide.csv")
        self.assertFalse(os.path.exists(self.tmpdir + "/vide.csv"))

    # add_stock_to_product
    def test_add_stock_to_product(self):
        self.inv.add_stock_to_product(self.product.product_id, 5, "Restock")
        self.assertEqual(self.inv.get_product(self.product.product_id).quantity, 15)
        self.assertEqual(len(self.inv.stock_moves), 1)
        self.assertEqual(self.inv.stock_moves[0].direction, "in")

    def test_add_stock_to_product_no_reason(self):
        self.inv.add_stock_to_product(self.product.product_id, 3)
        self.assertEqual(self.inv.get_product(self.product.product_id).quantity, 13)

    def test_add_stock_to_product_invalid_quantity_raise_error(self):
        with self.assertRaises(ValueError):
            self.inv.add_stock_to_product(self.product.product_id, 0)

    def test_add_stock_to_product_unknown_id_raise_error(self):
        with self.assertRaises(KeyError):
            self.inv.add_stock_to_product("UNKNOWN", 5)

    # remove_stock_from_product
    def test_remove_stock_from_product(self):
        self.inv.remove_stock_from_product(self.product.product_id, 3, "Vente")
        self.assertEqual(self.inv.get_product(self.product.product_id).quantity, 7)
        self.assertEqual(len(self.inv.stock_moves), 1)
        self.assertEqual(self.inv.stock_moves[0].direction, "out")

    def test_remove_stock_from_product_no_reason(self):
        self.inv.remove_stock_from_product(self.product.product_id, 2)
        self.assertEqual(self.inv.get_product(self.product.product_id).quantity, 8)

    def test_remove_stock_from_product_not_enough_raise_error(self):
        with self.assertRaises(ValueError):
            self.inv.remove_stock_from_product(self.product.product_id, 999)

    def test_remove_stock_from_product_unknown_id_raise_error(self):
        with self.assertRaises(KeyError):
            self.inv.remove_stock_from_product("UNKNOWN", 5)


######JSON PERSISTENCE#######
class TestInventoryPersistence(TestInventorySetup):

    def test_save_and_reload(self):
        p = self.inv.add_product("Laptop", 999.99, 10)
        c = self.inv.add_customer("Alice", "alice@example.com")
        o = self.inv.create_order(c.customer_id)
        o.add_line(self.inv.get_product(p.product_id), 2)
        self.inv.confirm_order(o.order_id)

        # reload
        with patch("Classes.inventory.DIR_DATA_FILES", self.tmpdir + "/"):
            inv2 = Inventory(
                filepathP  = "data_products.json",
                filepathC  = "data_customers.json",
                filepathO  = "data_orders.json",
                filepathSM = "data_stock_moves.json"
            )

        self.assertEqual(len(inv2.products),  1)
        self.assertEqual(len(inv2.customers), 1)
        self.assertEqual(len(inv2.orders),    1)

        p2 = inv2.get_product(p.product_id)
        self.assertEqual(p2.quantity, 8)        # decremented stock persisted

        o2 = inv2.get_order(o.order_id)
        self.assertEqual(o2.status,     "confirmed")
        self.assertEqual(len(o2.lines), 1)

    def test_stock_moves_persisted_after_reload(self):
        # stock moves created by confirm must survive a reload
        p = self.inv.add_product("Laptop", 999.99, 10)
        c = self.inv.add_customer("Alice", "alice@example.com")
        o = self.inv.create_order(c.customer_id)
        o.add_line(self.inv.get_product(p.product_id), 2)
        self.inv.confirm_order(o.order_id)

        with patch("Classes.inventory.DIR_DATA_FILES", self.tmpdir + "/"):
            inv2 = Inventory(
                filepathP  = "data_products.json",
                filepathC  = "data_customers.json",
                filepathO  = "data_orders.json",
                filepathSM = "data_stock_moves.json"
            )

        self.assertEqual(len(inv2.stock_moves), 1)
        self.assertEqual(inv2.stock_moves[0].direction, "out")

    def test_json_files_created(self):
        fichiers = [
            "data_products.json",
            "data_customers.json",
            "data_orders.json",
            "data_stock_moves.json"
        ]
        for f in fichiers:
            self.assertTrue(os.path.exists(os.path.join(self.tmpdir, f)))


if __name__ == "__main__":
    unittest.main()