import json
import os
import csv
from datetime import datetime
from config import DIR_DATA_FILES, ORDER_PREFIX, ORDER_NUMBERS
from Classes.product    import Product
from Classes.customer   import Customer
from Classes.order      import Order, OrderLine
from Classes.stock_move import StockMove
from Utils.db_connector import DBConnector
from Utils.queries import *

# ======================================================================
# JSON file paths (kept for previous version, before postgre DB
# ======================================================================
# DATA_FILE_PRODUCT  = "data_products.json"
# DATA_FILE_CUSTOMER = "data_customers.json"
# DATA_FILE_ORDER    = "data_orders.json"
# DATA_FILE_STMOV    = "data_stock_moves.json"


class Inventory:
    """
    Manages products, customers, orders and stock moves.
    Data is persisted in a PostgreSQL database via DBConnector.

    --- JSON structure (kept for reference, replaced by PostgreSQL) ---
    JSON PRODUCTS STRUCTURE :  { "products":    { product_id:  {...} } }
    JSON CUSTOMERS STRUCTURE : { "customers":   { customer_id: {...} } }
    JSON ORDERS STRUCTURE :    { "orders":      { order_id:    {...} } }
    JSON STOCKMOVES STRUCTURE: { "stock_moves": [ {product_id: ...} ] }
    """

    def __init__(self):
        self.products    = {}   # product_id  = Product
        self.customers   = {}   # customer_id = Customer
        self.orders      = {}   # order_id    = Order
        self.stock_moves = []
        self.db          = DBConnector()
        self.db.connect()
        self._load()


	#Load all data from PostgreSQL into memory."""
    def _load(self):
        #Products - (product_id, product_name, price, quantity, minimum_stock, category, active)
        cursor = self.db.execute(LIST_PRODUCTS)
        for row in cursor.fetchall():
            p = Product(
                product_id    = row[0],
                name          = row[1],
                price         = float(row[2]),
                quantity      = row[3],
                minimum_stock = row[4],
                category      = row[5],
                active        = row[6]
            )
            self.products[p.product_id] = p

        #Customers -(customer_id, customer_name, email, phone, active)
        cursor = self.db.execute(LIST_CUSTOMERS)
        for row in cursor.fetchall():
            c = Customer(
                customer_id = row[0],
                name        = row[1],
                email       = row[2],
                phone       = row[3],
                active      = row[4]
            )
            self.customers[c.customer_id] = c

        #Orders - (order_id, customer_id, customer_name, order_status, created_at, total)
        cursor = self.db.execute(LIST_ORDERS)
        for row in cursor.fetchall():
            customer = self.customers.get(row[1])
            if customer is None:
                continue  # customer not found -> ignore

            #order_lines - id, order_id, product_id, product_name, quantity, unit_price, subtotal)
            lines       = []
            line_cursor = self.db.execute(LIST_ORDER_LINES, (row[0],))
            for ld in line_cursor.fetchall():
                product = self.products.get(ld[2])
                if product is None:
                    continue  # product not found -> ignore
                line            = OrderLine(product, ld[4])
                line.unit_price = float(ld[5])
                lines.append(line)

            order = Order(
                order_id   = row[0],
                customer   = customer,
                lines      = lines,
                status     = row[3],
                created_at = str(row[4])
            )
            self.orders[order.order_id] = order

        #stock move - (id, product_id, product_name, quantity, direction, reason, created_at)
        cursor = self.db.execute(LIST_STOCK_MOVES)
        for row in cursor.fetchall():
            m = StockMove(
                product_id   = row[1],
                product_name = row[2],
                quantity     = row[3],
                direction    = row[4],
                reason       = row[5],
                created_at   = str(row[6])
            )
            self.stock_moves.append(m)

    # ------------------------------------------------------------------
    # JSON persistence (kept for reference, replaced by PostgreSQL)
    # ------------------------------------------------------------------
    '''
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
    '''

    # ID generation
    def _next_id(self, collection: dict, prefix: str) -> str:
        numbers = [
            int(k.replace(prefix, ""))
            for k in collection
            if str(k).startswith(prefix) and str(k).replace(prefix, "").isdigit()
        ]
        return f"{prefix}{(max(numbers) + 1) if numbers else 1}"

    def _next_order_sequence(self) -> str:
        year    = datetime.now().year
        numbers = []
        for oid in self.orders:
            parts = str(oid).split("/")
            if len(parts) == 3 and parts[0] == ORDER_PREFIX:
                if parts[2].isdigit():
                    numbers.append(int(parts[2]))
        next_num = (max(numbers) + 1) if numbers else 1
        return f"{ORDER_PREFIX}/{year}/{str(next_num).zfill(ORDER_NUMBERS)}"

    # Products
    def add_product(self, name, price, quantity, minimum_stock=5, category="General") -> Product:
        pid     = self._next_id(self.products, "P")
        product = Product(pid, name, price, quantity, minimum_stock, category)
        self.db.execute(CREATE_PRODUCT, (pid, name, price, quantity, minimum_stock, category, True))
        self.db.commit()
        self.products[pid] = product
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
        self.db.execute(ARCHIVE_PRODUCT, (product_id,))
        self.db.commit()

    # Stock
    def add_stock_to_product(self, product_id, amount, reason=""):
        product = self.get_product(product_id)
        move    = product.add_stock(amount, reason)
        self.db.execute(UPDATE_PRODUCT, (product.name, product.price, product.quantity, product_id))
        self._record_move(move)
        self.db.commit()

    def remove_stock_from_product(self, product_id, amount, reason=""):
        product = self.get_product(product_id)
        move    = product.remove_stock(amount, reason)
        self.db.execute(UPDATE_PRODUCT, (product.name, product.price, product.quantity, product_id))
        self._record_move(move)
        self.db.commit()

    # Customers
    def add_customer(self, name, email, phone="") -> Customer:
        cid      = self._next_id(self.customers, "C")
        customer = Customer(cid, name, email, phone)
        self.db.execute(CREATE_CUSTOMER, (cid, name, email, phone, True))
        self.db.commit()
        self.customers[cid] = customer
        return customer

    def get_customer(self, customer_id) -> Customer:
        c = self.customers.get(customer_id)
        if c is None:
            raise KeyError(f"Customer not found : {customer_id!r}")
        return c

    def list_customers(self, include_archived=False) -> list:
        return [
            c for c in self.customers.values()
            if include_archived or c.active
        ]

    # Orders
    def create_order(self, customer_id) -> Order:
        customer = self.get_customer(customer_id)
        oid      = self._next_order_sequence()
        order    = Order(oid, customer)
        self.db.execute(CREATE_ORDER, (oid, customer_id, customer.name, "draft", order.created_at))
        self.db.commit()
        self.orders[oid] = order
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

        # Update order status in DB
        self.db.execute(UPDATE_ORDER, ("confirmed", order_id))

        # Update stock quantity for each line + insert order lines + trace stock moves
        for line in order.lines:
            self.db.execute(UPDATE_PRODUCT, (
                line.product.name,
                line.product.price,
                line.product.quantity,
                line.product.product_id
            ))
            self.db.execute(ADD_ORDER_LINES, (
                order_id,
                line.product.product_id,
                line.product.name,
                line.quantity,
                line.unit_price,
                line.subtotal
            ))
            move = StockMove(
                line.product.product_id,
                line.product.name,
                line.quantity,
                "out",
                reason=f"Order {order.order_id}"
            )
            self._record_move(move)

        self.db.commit()

    def cancel_order(self, order_id):
        order         = self.get_order(order_id)
        was_confirmed = order.status == "confirmed"  # capture BEFORE cancel()
        order.cancel()

        self.db.execute(UPDATE_ORDER, ("cancelled", order_id))

        # Restock if order was confirmed
        if was_confirmed:
            for line in order.lines:
                self.db.execute(UPDATE_PRODUCT, (
                    line.product.name,
                    line.product.price,
                    line.product.quantity,
                    line.product.product_id
                ))
                move = StockMove(
                    line.product.product_id,
                    line.product.name,
                    line.quantity,
                    "in",
                    reason=f"Cancelled order {order.order_id}"
                )
                self._record_move(move)

        self.db.commit()

    def mark_order_done(self, order_id):
        self.get_order(order_id).mark_done()
        self.db.execute(UPDATE_ORDER, ("done", order_id))
        self.db.commit()

    # Reports
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

    # Stock moves
    def _record_move(self, move):   #_ because not supposed to be called from outside
        if move:
            self.stock_moves.append(move)
            self.db.execute(INSERT_STOCK_MOVES, (
                move.product_id,
                move.product_name,
                move.quantity,
                move.direction,
                move.reason,
                move.created_at
            ))

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

    # Display
    def __repr__(self):
        return (
            f"Inventory(products={len(self.products)}, "
            f"customers={len(self.customers)}, "
            f"orders={len(self.orders)}, "
            f"stock_moves={len(self.stock_moves)})"
        )
