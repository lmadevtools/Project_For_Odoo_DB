import unittest
from Classes.customer import Customer


class TestCustomerInit(unittest.TestCase):

    def test_creation_correct(self):
        c = Customer("C1", "Alice Martin", "alice@example.com", "06 11 22 33 44")
        self.assertEqual(c.customer_id, "C1")
        self.assertEqual(c.name,        "Alice Martin")
        self.assertEqual(c.email,       "alice@example.com")
        self.assertEqual(c.phone,       "06 11 22 33 44")
        self.assertTrue(c.active)

    def test_email_normalise_minuscules(self):
        c = Customer("C1", "Alice", "ALICE@EXAMPLE.COM")
        self.assertEqual(c.email, "alice@example.com")

    def test_nom_stripe(self):
        c = Customer("C1", "  Bob  ", "bob@example.com")
        self.assertEqual(c.name, "Bob")

    def test_phone_optionnal(self):
        c = Customer("C1", "Alice", "alice@example.com")
        self.assertEqual(c.phone, "")

    def test_email_invalid_sans_arobase_raise_error(self):
        with self.assertRaises(ValueError):
            Customer("C1", "Alice", "aliceexample.com")

    def test_email_invalid_sans_point_raise_error(self):
        with self.assertRaises(ValueError):
            Customer("C1", "Alice", "alice@examplecom")

    def test_no_mail_raise_error(self):
        with self.assertRaises((ValueError, TypeError)):
            Customer("C1", "Alice", None)

    def test_empty_name_raise_error(self):
        with self.assertRaises(ValueError):
            Customer("C1", "", "alice@example.com")

    def test_name_spaces_raise_error(self):
        with self.assertRaises(ValueError):
            Customer("C1", "   ", "alice@example.com")

    def test_empty_id_raise_error(self):
        with self.assertRaises(ValueError):
            Customer("", "Alice", "alice@example.com")
			
class TestCustomerSetters(unittest.TestCase):

    def setUp(self):
        self.c = Customer("C1", "Alice", "alice@example.com", "06 11 22 33 44")

    # customer_id — read only
    def test_customer_id_read_only(self):
        with self.assertRaises(AttributeError):
            self.c.customer_id = "C99"

    # name
    def test_set_name_validity(self):
        self.c.name = "Bob"
        self.assertEqual(self.c.name, "Bob")

    def test_set_name_strip(self):
        self.c.name = "  Bob  "
        self.assertEqual(self.c.name, "Bob")

    def test_set_name_empty_raise_error(self):
        with self.assertRaises(ValueError):
            self.c.name = ""

    # email
    def test_set_email_validity(self):
        self.c.email = "BOB@EXAMPLE.COM"
        self.assertEqual(self.c.email, "bob@example.com")   # lowercase applied 

    def test_set_invalid_email_raise_error(self):
        with self.assertRaises(ValueError):
            self.c.email = "notanemail"

    # phone
    def test_set_phone_valid(self):
        self.c.phone = "  07 99 88 77 66  "
        self.assertEqual(self.c.phone, "07 99 88 77 66")    # strip applied

    def test_set_phone_empty(self):
        self.c.phone = ""
        self.assertEqual(self.c.phone, "")


class TestCustomerArchive(unittest.TestCase):

    def setUp(self):
        self.c = Customer("C1", "Alice", "alice@example.com")

    def test_archive(self):
        self.c.archive()
        self.assertFalse(self.c.active)

    def test_unarchive(self):
        self.c.archive()
        self.c.unarchive()
        self.assertTrue(self.c.active)

#OLD SERIALIZATION JSON TEST
'''
class TestCustomerSerialization(unittest.TestCase):

    def setUp(self):
        self.c = Customer("C1", "Alice Martin", "alice@example.com", "06 11 22 33 44")

    def test_to_dict(self):
        d = self.c.to_dict()
        self.assertEqual(d["customer_id"], "C1")
        self.assertEqual(d["name"],        "Alice Martin")
        self.assertEqual(d["email"],       "alice@example.com")
        self.assertEqual(d["phone"],       "06 11 22 33 44")
        self.assertTrue(d["active"])

    def test_from_dict_roundtrip(self):
        d  = self.c.to_dict()
        c2 = Customer.from_dict(d)
        self.assertEqual(c2.customer_id, self.c.customer_id)
        self.assertEqual(c2.name,        self.c.name)
        self.assertEqual(c2.email,       self.c.email)
        self.assertEqual(c2.phone,       self.c.phone)

    def test_from_dict_phone_optionnal(self):
        d = {"customer_id": "C2", "name": "Bob", "email": "bob@example.com"}
        c = Customer.from_dict(d)
        self.assertEqual(c.phone, "")
        self.assertTrue(c.active)

    def test_from_dict_missing_field_raise_error(self):
        with self.assertRaises(KeyError):
            Customer.from_dict({"customer_id": "C1", "name": "Alice"})  # missing email
'''

if __name__ == "__main__":
    unittest.main()
