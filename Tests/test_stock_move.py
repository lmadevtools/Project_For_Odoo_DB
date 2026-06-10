import unittest
from Classes.stock_move import StockMove


class TestStockMoveInit(unittest.TestCase):

    def test_creation_in(self):
        m = StockMove("P1", "Laptop", 10, "in", "Restock")
        self.assertEqual(m.product_id,   "P1")
        self.assertEqual(m.product_name, "Laptop")
        self.assertEqual(m.quantity,     10)
        self.assertEqual(m.direction,    "in")
        self.assertEqual(m.reason,       "Restock")

    def test_creation_out(self):
        m = StockMove("P1", "Laptop", 5, "out")
        self.assertEqual(m.direction, "out")
        self.assertEqual(m.reason,    "")

    def test_created_at_auto(self):
        m = StockMove("P1", "Laptop", 1, "in")
        self.assertIsNotNone(m.created_at)
        self.assertRegex(m.created_at, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_created_at_by_user(self):
        m = StockMove("P1", "Laptop", 1, "in", created_at="2025-01-01 10:00:00")
        self.assertEqual(m.created_at, "2025-01-01 10:00:00")

    def test_invalid_direction_raise_error(self):
        with self.assertRaises(ValueError):
            StockMove("P1", "Laptop", 10, "unknown")

    def test_zero_quantity_raise_error(self):
        with self.assertRaises(ValueError):
            StockMove("P1", "Laptop", 0, "in")

    def test_negative_quantity_raise_error(self):
        with self.assertRaises(ValueError):
            StockMove("P1", "Laptop", -5, "in")
			
class TestStockMoveReadOnly(unittest.TestCase):

    def setUp(self):
        self.m = StockMove("P1", "Laptop", 10, "in", "Restock")

    def test_product_id_read_only(self):
        with self.assertRaises(AttributeError):
            self.m.product_id = "P99"

    def test_quantity_read_only(self):
        with self.assertRaises(AttributeError):
            self.m.quantity = 999

    def test_direction_read_only(self):
        with self.assertRaises(AttributeError):
            self.m.direction = "out"

    def test_created_at_read_only(self):
        with self.assertRaises(AttributeError):
            self.m.created_at = "2099-01-01"

class TestStockMoveSerialization(unittest.TestCase):

    def setUp(self):
        self.m = StockMove("P1", "Laptop", 10, "in", "Restock", "2025-01-01 10:00:00")

    def test_to_dict(self):
        d = self.m.to_dict()
        self.assertEqual(d["product_id"],   "P1")
        self.assertEqual(d["product_name"], "Laptop")
        self.assertEqual(d["quantity"],     10)
        self.assertEqual(d["direction"],    "in")
        self.assertEqual(d["reason"],       "Restock")
        self.assertEqual(d["created_at"],   "2025-01-01 10:00:00")

#OLD SERIALIZATION JSON TEST
'''
    def test_from_dict_roundtrip(self):
        d  = self.m.to_dict()
        m2 = StockMove.from_dict(d)
        self.assertEqual(m2.product_id,   self.m.product_id)
        self.assertEqual(m2.product_name, self.m.product_name)
        self.assertEqual(m2.quantity,     self.m.quantity)
        self.assertEqual(m2.direction,    self.m.direction)
        self.assertEqual(m2.reason,       self.m.reason)
        self.assertEqual(m2.created_at,   self.m.created_at)
'''


if __name__ == "__main__":
    unittest.main()
