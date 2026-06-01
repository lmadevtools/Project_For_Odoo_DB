import json
import os
import csv 
from datetime import datetime
from config import DIR_DATA_FILES
from config import ORDER_PREFIX
from config import ORDER_NUMBERS
from Classes.product  import Product
from Classes.customer import Customer
from Classes.order    import Order, OrderLine
from Classes.stock_move import StockMove

DATA_FILE_PRODUCT  = "data_products.json"
DATA_FILE_CUSTOMER = "data_customers.json"
DATA_FILE_ORDER    = "data_orders.json"
DATA_FILE_STMOV    = "data_stock_moves.json"

class Inventory:
    """
    JSON PRODUCTS STRUCTURE :
    {
        "products":  { product_id:  {...} }
    }
    JSON CUSTOMERS STRUCTURE :
    {
        "customers": { customer_id: {...} }
    }
    JSON ORDERS STRUCTURE :
    {
        "orders":    { order_id:    {...} }
    }
    JSON STOCKMOVES STRUCTURE :
    {
        "stock_moves":    [ {product_id: ...} ]
    }
    """

    def __init__(self, filepathP=DATA_FILE_PRODUCT, filepathC=DATA_FILE_CUSTOMER, filepathO=DATA_FILE_ORDER, filepathSM=DATA_FILE_STMOV):
        self.filepathP  = DIR_DATA_FILES + filepathP
        self.filepathC  = DIR_DATA_FILES + filepathC
        self.filepathO  = DIR_DATA_FILES + filepathO
        self.filepathSM = DIR_DATA_FILES + filepathSM
        self.products    = {}   # product_id  = Product
        self.customers   = {}   # customer_id = Customer
        self.orders      = {}   # order_id    = Order
        self.stock_moves = []
        self._load()

    # Persistence for JSON
    def _load(self):    #_ because not supposed to be called from outside
        #load data from JSON file and create if not found
        if not os.path.exists(self.filepathP):    #if file doesn't exist -> quit, cause we need product for orders
            self._save()
            return
        if not os.path.exists(self.filepathC):    #if file doesn't exist -> quit, cause we need customers for orders
            self._save()
            return
        if not os.path.exists(self.filepathO):    #orders
            self._save()
            return
        if not os.path.exists(self.filepathSM):   #stock_moves
            self._save()
            return

        #products
        with open(self.filepathP, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for data in raw.get("products", {}).values():
            p = Product.from_dict(data)
            self.products[p.product_id] = p

        #customers
        with open(self.filepathC, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for data in raw.get("customers", {}).values():
            c = Customer.from_dict(data)
            self.customers[c.customer_id] = c

        #orders (linked to already loaded products and customers)
        with open(self.filepathO, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for data in raw.get("orders", {}).values():
            customer = self.customers.get(data["customer_id"])
            if customer is None:
                continue  # not found -> ignore

            lines = []
            for ld in data.get("lines", []):
                product = self.products.get(ld["product_id"])
                if product is None:
                    continue  # not found -> ignore
                line = OrderLine(product, ld["quantity"])
                line.unit_price = ld["unit_price"]
                lines.append(line)

            order = Order(
                order_id   = data["order_id"],
                customer   = customer,
                lines      = lines,
                status     = data["status"],
                created_at = data["created_at"]
            )
            self.orders[order.order_id] = order

        #stock_moves
        with open(self.filepathSM, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for data in raw.get("stock_moves", []):
            self.stock_moves.append(StockMove.from_dict(data))

    def _save(self):    #_ because not supposed to be called from outside
        #save into json file
        if not os.path.isdir(DIR_DATA_FILES):
            os.mkdir(DIR_DATA_FILES)

        dataP  = {"products":   {pid: p.to_dict() for pid, p in self.products.items()}}
        dataC  = {"customers":  {cid: c.to_dict() for cid, c in self.customers.items()}}
        dataO  = {"orders":     {oid: o.to_dict() for oid, o in self.orders.items()}}
        dataSM = {"stock_moves": [m.to_dict() for m in self.stock_moves]}

        with open(self.filepathP,  "w", encoding="utf-8") as f:
            json.dump(dataP,  f, ensure_ascii=False, indent=2)
        with open(self.filepathC,  "w", encoding="utf-8") as f:
            json.dump(dataC,  f, ensure_ascii=False, indent=2)
        with open(self.filepathO,  "w", encoding="utf-8") as f:
            json.dump(dataO,  f, ensure_ascii=False, indent=2)
        with open(self.filepathSM, "w", encoding="utf-8") as f:
            json.dump(dataSM, f, ensure_ascii=False, indent=2)

    #ID generation
    def _next_id(self, collection: dict, prefix: str) -> str:   #_ because not supposed to be called from outside
        numbers = [
            int(k.replace(prefix, ""))
            for k in collection
            if str(k).startswith(prefix) and str(k).replace(prefix, "").isdigit()
        ]
        return f"{prefix}{(max(numbers) + 1) if numbers else 1}"

    def _next_order_sequence(self):     #_ because not supposed to be called from outside
        year = datetime.now().year
        numbers = []
        for oid in self.orders:
            # CMD/YEAR/XXXX where XXXX is a number based on ORDER_NUMBERS param in config.py
            parts = str(oid).split("/")
            if len(parts) == 3 and parts[0] == ORDER_PREFIX:
                if parts[2].isdigit():
                    numbers.append(int(parts[2]))
        next_num = (max(numbers) + 1) if numbers else 1
        return f"{ORDER_PREFIX}/{year}/{str(next_num).zfill(ORDER_NUMBERS)}"

    #Products
    def add_product(self, name, price, quantity, minimum_stock=5, category="General") -> Product:
        pid     = self._next_id(self.products, "P")
        product = Product(pid, name, price, quantity, minimum_stock, category)
        self.products[pid] = product
        self._save()
        return product

    def get_product(self, product_id) -> Product:
        p = self.products.get(product_id)
        if p is None:
            raise KeyError(f"Product not found : {product_id!r}")
        return p

    def list_products(self, include_archived=False) -> list:
        return [
            p for p in self.products.values()
            if include_archived or p.active
        ]

    def list_low_stock(self) -> list:
        return [p for p in self.list_products() if p.is_low_stock()]

    def archive_product(self, product_id):
        self.get_product(product_id).archive()
        self._save()

	#Stock
    def add_stock_to_product(self, product_id, amount, reason=""):
        product = self.get_product(product_id)
        move    = product.add_stock(amount, reason)
        self._record_move(move)
        self._save()
        return move

    def remove_stock_from_product(self, product_id, amount, reason=""):
        product = self.get_product(product_id)
        move    = product.remove_stock(amount, reason)
        self._record_move(move)
        self._save()
        return move

	#Customers
    def add_customer(self, name, email, phone="") -> Customer:
        cid      = self._next_id(self.customers, "C")
        customer = Customer(cid, name, email, phone)
        self.customers[cid] = customer
        self._save()
        return customer

    def get_customer(self, customer_id) -> Customer:
        c = self.customers.get(customer_id)
        if c is None:
            raise KeyError(f"Client not found : {customer_id!r}")
        return c

    def list_customers(self, include_archived=False) -> list:
        return [
            c for c in self.customers.values()
            if include_archived or c.active
        ]

	#Orders
    def create_order(self, customer_id) -> Order:
        customer = self.get_customer(customer_id)
        oid      = self._next_order_sequence()      # CMD/2026/0001
        order    = Order(oid, customer)
        self.orders[oid] = order
        self._save()
        return order

    def get_order(self, order_id) -> Order:
        o = self.orders.get(order_id)
        if o is None:
            raise KeyError(f"Order not found : {order_id!r}")
        return o

    def list_orders(self, status=None) -> list:
        orders = list(self.orders.values())
        if status:
            orders = [o for o in orders if o.status == status]
        return orders

    def confirm_order(self, order_id):
        order = self.get_order(order_id)
        order.confirm()

        # Trace a stock move for each line
        for line in order.lines:
            self._record_move(StockMove(
                line.product.product_id,
                line.product.name,
                line.quantity,
                "out",
                reason=f"Order {order.order_id}"
            ))

        self._save()

    def cancel_order(self, order_id):
        order         = self.get_order(order_id)
        was_confirmed = order.status == "confirmed"  # capture BEFORE cancel()
        order.cancel()

        # Restock moves only if order was confirmed (stock was decremented)
        if was_confirmed:
            for line in order.lines:
                self._record_move(StockMove(
                    line.product.product_id,
                    line.product.name,
                    line.quantity,
                    "in",
                    reason=f"Cancelled order {order.order_id}"
                ))

        self._save()

    def mark_order_done(self, order_id):
        self.get_order(order_id).mark_done()
        self._save()

    #Reports
    def report_stock(self):
        print("\n=== REPORT STOCK ===")
        for p in self.list_products():
            print(p)
        print()

    def report_low_stock(self):
        low = self.list_low_stock()
        print(f"\n=== LOW STOCK ({len(low)} product(s)) ===")
        for p in low:
            print(p)
        print()

    def report_orders(self, status=None):
        orders = self.list_orders(status)
        label  = status.upper() if status else "ALL"
        print(f"\n=== ORDER [{label}] ({len(orders)}) ===")
        for o in orders:
            print(o)
            print()

	#StockMoves
    def _record_move(self, move):   #_ because not supposed to be called from outside
        if move:
            self.stock_moves.append(move)

    def export_csv(self, filepath="export.csv"):
        if not self.stock_moves:
            print("No move to export")
            return

        with open(DIR_DATA_FILES + filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "created_at", "product_id", "product_name", "direction", "quantity", "reason"
            ])
            writer.writeheader()
            for move in self.stock_moves:
                writer.writerow(move.to_dict())

        print(f"CSV Exported : {filepath} ({len(self.stock_moves)} rows)")

	#Display
    def __repr__(self):
        return (
            f"Inventory(products={len(self.products)}, "
            f"customers={len(self.customers)}, "
            f"orders={len(self.orders)}, "
            f"stock_moves={len(self.stock_moves)})"
        )
