import unittest
from Classes.product    import Product
from Classes.stock_move import StockMove


class TestProductInit(unittest.TestCase):

    def test_creation_valid(self):
        p = Product("P1", "Laptop", 999.99, 10)
        self.assertEqual(p.product_id,    "P1")
        self.assertEqual(p.name,          "Laptop")
        self.assertEqual(p.price,         999.99)
        self.assertEqual(p.quantity,      10)
        self.assertEqual(p.minimum_stock, 5)
        self.assertEqual(p.category,      "General")
        self.assertTrue(p.active)

    def test_name_stripe(self):
        p = Product("P1", "  Laptop  ", 10.0, 5)
        self.assertEqual(p.name, "Laptop")

    def test_creation_with_options(self):
        p = Product("P1", "Laptop", 999.99, 10, minimum_stock=3, category="Informatique")
        self.assertEqual(p.minimum_stock, 3)
        self.assertEqual(p.category,      "Informatique")

    def test_negative_price_raise_error(self):
        with self.assertRaises(ValueError):
            Product("P1", "Laptop", -1.0, 10)

    def test_negative_quantity_raise_error(self):
        with self.assertRaises(ValueError):
            Product("P1", "Laptop", 10.0, -5)

    def test_negative_minimum_stock_raise_error(self):
        with self.assertRaises(ValueError):
            Product("P1", "Laptop", 10.0, 5, minimum_stock=-1)

    def test_empty_name_raise_error(self):
        with self.assertRaises(ValueError):
            Product("P1", "", 10.0, 5)

    def test_name_spaces_raise_error(self):
        with self.assertRaises(ValueError):
            Product("P1", "   ", 10.0, 5)

    def test_empty_id_raise_error(self):
        with self.assertRaises(ValueError):
            Product("", "Laptop", 10.0, 5)

class TestProductSetters(unittest.TestCase):

    def setUp(self):
        self.p = Product("P1", "Laptop", 999.99, 10)

    # product_id — read only
    def test_product_id_read_only(self):
        with self.assertRaises(AttributeError):
            self.p.product_id = "P99"

    # name
    def test_set_name_valid(self):
        self.p.name = "New Laptop"
        self.assertEqual(self.p.name, "New Laptop")

    def test_set_name_strip(self):
        self.p.name = "  New Laptop  "
        self.assertEqual(self.p.name, "New Laptop")

    def test_set_name_empty_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.name = ""

    def test_set_name_spaces_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.name = "   "

    # price
    def test_set_price_valid(self):
        self.p.price = 499.99
        self.assertEqual(self.p.price, 499.99)

    def test_set_price_zero_valid(self):
        self.p.price = 0
        self.assertEqual(self.p.price, 0)

    def test_set_negative_prce_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.price = -10

    # quantity — read only 
    def test_quantity_read_only(self):
        with self.assertRaises(AttributeError):
            self.p.quantity = 999

    # minimum_stock
    def test_set_minimum_stock_valid(self):
        self.p.minimum_stock = 10
        self.assertEqual(self.p.minimum_stock, 10)

    def test_set_minimum_stock_negative_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.minimum_stock = -1

class TestProductStock(unittest.TestCase):

    def setUp(self):
        self.p = Product("P1", "Laptop", 999.99, 20, minimum_stock=5)

    def test_add_stock_return_stock_move(self):
        move = self.p.add_stock(10)
        self.assertIsInstance(move, StockMove)
        self.assertEqual(move.direction, "in")
        self.assertEqual(move.quantity,  10)

    def test_add_stock_update_quantity(self):
        self.p.add_stock(10)
        self.assertEqual(self.p.quantity, 30)

    def test_add_stock_with_reason(self):
        move = self.p.add_stock(5, reason="Restock fournisseur")
        self.assertEqual(move.reason, "Restock fournisseur")

    def test_remove_stock_return_stock_move(self):
        move = self.p.remove_stock(5)
        self.assertIsInstance(move, StockMove)
        self.assertEqual(move.direction, "out")
        self.assertEqual(move.quantity,  5)

    def test_remove_stock_update_quantity(self):
        self.p.remove_stock(5)
        self.assertEqual(self.p.quantity, 15)

    def test_remove_exact_stockt(self):
        self.p.remove_stock(20)
        self.assertEqual(self.p.quantity, 0)

    def test_add_stock_zero_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.add_stock(0)

    def test_add_negative_stock_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.add_stock(-5)

    def test_remove_stock_zero_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.remove_stock(0)

    def test_remove_stock_not_enough_raise_error(self):
        with self.assertRaises(ValueError):
            self.p.remove_stock(999)

    def test_quantity_not_updated_if_error(self):
        try:
            self.p.remove_stock(999)
        except ValueError:
            pass
        self.assertEqual(self.p.quantity, 20)


class TestProductLowStock(unittest.TestCase):

    def test_low_stock_under(self):
        p = Product("P1", "Test", 10.0, 3, minimum_stock=5)
        self.assertTrue(p.is_low_stock())

    def test_low_stock_egal(self):
        p = Product("P1", "Test", 10.0, 5, minimum_stock=5)
        self.assertTrue(p.is_low_stock())

    def test_low_stock_over(self):
        p = Product("P1", "Test", 10.0, 6, minimum_stock=5)
        self.assertFalse(p.is_low_stock())


class TestProductArchive(unittest.TestCase):

    def setUp(self):
        self.p = Product("P1", "Test", 10.0, 10)

    def test_archive(self):
        self.p.archive()
        self.assertFalse(self.p.active)

    def test_unarchive(self):
        self.p.archive()
        self.p.unarchive()
        self.assertTrue(self.p.active)


class TestProductSerialization(unittest.TestCase):

    def setUp(self):
        self.p = Product("P1", "Laptop", 999.99, 10, minimum_stock=3, category="Informatique")

    def test_to_dict(self):
        d = self.p.to_dict()
        self.assertEqual(d["product_id"],    "P1")
        self.assertEqual(d["name"],          "Laptop")
        self.assertEqual(d["price"],         999.99)
        self.assertEqual(d["quantity"],      10)
        self.assertEqual(d["minimum_stock"], 3)
        self.assertEqual(d["category"],      "Informatique")
        self.assertTrue(d["active"])

    def test_from_dict_roundtrip(self):
        d  = self.p.to_dict()
        p2 = Product.from_dict(d)
        self.assertEqual(p2.product_id, self.p.product_id)
        self.assertEqual(p2.name,       self.p.name)
        self.assertEqual(p2.price,      self.p.price)
        self.assertEqual(p2.quantity,   self.p.quantity)

    def test_from_dict_optionnals_values(self):
        d = {"product_id": "P2", "name": "Souris", "price": 29.99, "quantity": 5}
        p = Product.from_dict(d)
        self.assertEqual(p.minimum_stock, 10)    # def val in from_dict
        self.assertEqual(p.category,      "General")
        self.assertTrue(p.active)

    def test_from_dict_missing_field_raise_error(self):
        with self.assertRaises(KeyError):
            Product.from_dict({"product_id": "P1", "name": "Test"})


if __name__ == "__main__":
    unittest.main()
