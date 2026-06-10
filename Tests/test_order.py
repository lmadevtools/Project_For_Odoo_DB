import unittest
from Classes.product  import Product
from Classes.customer import Customer
from Classes.order    import Order, OrderLine


def make_product(pid="P1", name="Laptop", price=1000.0, quantity=10):
    return Product(pid, name, price, quantity)

def make_customer(cid="C1", name="Alice", email="alice@example.com"):
    return Customer(cid, name, email)

def make_order(order_id="O1", customer=None):
    return Order(order_id, customer or make_customer())


######ORDER LINE#######
class TestOrderLineInit(unittest.TestCase):

    def test_creation_valid(self):
        line = OrderLine(make_product(price=99.99), 3)
        self.assertEqual(line.quantity,   3)
        self.assertEqual(line.unit_price, 99.99)

    def test_fixed_price_at_creation(self):
        p    = make_product(price=100.0)
        line = OrderLine(p, 2)
        p.price = 200.0
        self.assertEqual(line.unit_price, 100.0)   # prix non impacte

    def test_zero_quantity_raise_error(self):
        with self.assertRaises(ValueError):
            OrderLine(make_product(), 0)

    def test_negative_quantity_raise_error(self):
        with self.assertRaises(ValueError):
            OrderLine(make_product(), -3)


class TestOrderLineSubtotal(unittest.TestCase):

    def test_subtotal(self):
        line = OrderLine(make_product(price=29.99), 3)
        self.assertAlmostEqual(line.subtotal, 89.97)

    def test_subtotal_rounded(self):
        line = OrderLine(make_product(price=0.1), 3)
        self.assertEqual(line.subtotal, 0.3)


######ORDER INIT#######
class TestOrderInit(unittest.TestCase):

    def test_creation_valid(self):
        o = make_order()
        self.assertEqual(o.order_id, "O1")
        self.assertEqual(o.status,   "draft")
        self.assertEqual(o.lines,    [])

    def test_invalid_status_raise_error(self):
        with self.assertRaises(ValueError):
            Order("O1", make_customer(), status="unknown")

    def test_order_empty_id_raise_error(self):
        with self.assertRaises(ValueError):
            Order("", make_customer())

######ORDER LINE#######
class TestOrderLines(unittest.TestCase):

    def setUp(self):
        self.order   = make_order()
        self.product = make_product()

    def test_add_line(self):
        self.order.add_line(self.product, 2)
        self.assertEqual(len(self.order.lines),        1)
        self.assertEqual(self.order.lines[0].quantity, 2)

    def test_add_line_same_product_added(self):
        self.order.add_line(self.product, 2)
        self.order.add_line(self.product, 3)
        self.assertEqual(len(self.order.lines),        1)
        self.assertEqual(self.order.lines[0].quantity, 5)

    def test_add_line_product_archive_raise_error(self):
        self.product.archive()
        with self.assertRaises(ValueError):
            self.order.add_line(self.product, 1)

    def test_add_line_order_not_draft_raise_error(self):
        self.order.add_line(self.product, 1)
        self.order.confirm()
        with self.assertRaises(RuntimeError):
            self.order.add_line(self.product, 1)

    def test_remove_line(self):
        self.order.add_line(self.product, 2)
        self.order.remove_line(self.product.product_id)
        self.assertEqual(len(self.order.lines), 0)

    def test_remove_line_unknown_raise_error(self):
        with self.assertRaises(ValueError):
            self.order.remove_line("INCONNU")

    def test_remove_line_order_not_draft_raise_error(self):
        self.order.add_line(self.product, 1)
        self.order.confirm()
        with self.assertRaises(RuntimeError):
            self.order.remove_line(self.product.product_id)


######ORDER WORKFLOW#######
class TestOrderWorkflow(unittest.TestCase):

    def setUp(self):
        self.product = make_product(quantity=10)
        self.order   = make_order()
        self.order.add_line(self.product, 3)

    def test_confirm_pass_to_confirmed(self):
        self.order.confirm()
        self.assertEqual(self.order.status, "confirmed")

    def test_confirm_dec_stock(self):
        self.order.confirm()
        self.assertEqual(self.product.quantity, 7)

    def test_confirm_no_lines_raise_error(self):
        o = make_order(order_id="O2")
        with self.assertRaises(RuntimeError):
            o.confirm()

    def test_confirm_not_enough_stock_raise_error(self):
        self.order.add_line(make_product(pid="P2", quantity=1), 999)
        with self.assertRaises(ValueError):
            self.order.confirm()

    def test_confirm_twice_raise_error(self):
        self.order.confirm()
        with self.assertRaises(RuntimeError):
            self.order.confirm()

    def test_mark_done(self):
        self.order.confirm()
        self.order.mark_done()
        self.assertEqual(self.order.status, "done")

    def test_mark_done_without_confirm_raise_error(self):
        with self.assertRaises(RuntimeError):
            self.order.mark_done()

    def test_cancel_from_draft(self):
        self.order.cancel()
        self.assertEqual(self.order.status, "cancelled")

    def test_cancel_from_confirmed_restitue_stock(self):
        self.order.confirm()
        self.assertEqual(self.product.quantity, 7)
        self.order.cancel()
        self.assertEqual(self.product.quantity, 10)

    def test_cancel_from_done_raise_error(self):
        self.order.confirm()
        self.order.mark_done()
        with self.assertRaises(RuntimeError):
            self.order.cancel()

    def test_cancel_twice_raise_error(self):
        self.order.cancel()
        with self.assertRaises(RuntimeError):
            self.order.cancel()


#######ORDER TOTAL#######
class TestOrderTotal(unittest.TestCase):

    def test_total_empty(self):
        self.assertEqual(make_order().total, 0)

    def test_total_one_row(self):
        o = make_order()
        o.add_line(make_product(price=100.0), 3)
        self.assertAlmostEqual(o.total, 300.0)

    def test_total_multi_rows(self):
        o = make_order()
        o.add_line(make_product(pid="P1", price=100.0), 2)
        o.add_line(make_product(pid="P2", price=50.0),  3)
        self.assertAlmostEqual(o.total, 350.0)


#OLD SERIALIZATION JSON TEST
'''
class TestOrderSerialization(unittest.TestCase):

    def test_to_dict(self):
        o = make_order()
        o.add_line(make_product(price=100.0), 2)
        d = o.to_dict()
        self.assertEqual(d["order_id"], "O1")
        self.assertEqual(d["status"],   "draft")
        self.assertEqual(len(d["lines"]), 1)
        self.assertAlmostEqual(d["total"], 200.0)
'''

if __name__ == "__main__":
    unittest.main()
