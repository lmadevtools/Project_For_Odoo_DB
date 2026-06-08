from Utils.helper import log_message
from Classes.inventory import Inventory

inv = Inventory()

#Helpers
def separator():
    print("\n" + "=" * 50)

def pause():
    input("\nEnter to continue")

def prompt_int(label, min_val=None):
    while True:
        try:
            val = int(input(f"{label} : "))
            if min_val is not None and val < min_val:
                print(f"  minimum value : {min_val}")
                continue
            return val
        except ValueError:
            print("  integer awaited")

def prompt_float(label, min_val=None):
    while True:
        try:
            val = float(input(f"{label} : "))
            if min_val is not None and val < min_val:
                print(f"  minimum value : {min_val}")
                continue
            return val
        except ValueError:
            print("  number awaited")

def prompt_str(label, required=True):
    while True:
        val = input(f"{label} : ").strip()
        if required and not val:
            print("  mandatory field")
            continue
        return val

def choose(options: list, label="Choice") -> str:
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            idx = int(input(f"{label} : "))
            if 1 <= idx <= len(options):
                return options[idx - 1]
            print(f"  between 1 and {len(options)}")
        except ValueError:
            print("  integer awaited")


#Products
def menu_produits():
    while True:
        separator()
        print("  PRODUCTS")
        separator()
        print("  1. List all products")
        print("  2. Add a product")
        print("  3. Add stock")
        print("  4. Remove stock")
        print("  5. Archive a product")
        print("  0. Back")
        separator()

        choix = input("Choice : ").strip()

        if choix == "1":
            lister_produits()
        elif choix == "2":
            ajouter_produit()
        elif choix == "3":
            modifier_stock("in")
        elif choix == "4":
            modifier_stock("out")
        elif choix == "5":
            archiver_produit()
        elif choix == "0":
            break
        else:
            print("  Invalid choice")


def lister_produits():
    separator()
    produits = inv.list_products()
    if not produits:
        print("  No product.")
        pause()
        return
    for p in produits:
        print(f"  {p}")
    pause()


def ajouter_produit():
    separator()
    print("  NEW PRODUCT")
    separator()
    try:
        name          = prompt_str("Name")
        price         = prompt_float("Price (€)", min_val=0)
        quantity      = prompt_int("Quantity", min_val=0)
        minimum_stock = prompt_int("Minimum stock", min_val=0)
        category      = prompt_str("Category (def : General)", required=False) or "General"

        p = inv.add_product(name, price, quantity, minimum_stock, category)
        log_message(f"Product created : {p.product_id} - {p.name}", "info")
        print(f"\n  Product created : {p}")
    except ValueError as e:
        log_message(f"Error creating product : {e}", "error")
        print(f"  Error : {e}")
    pause()


def modifier_stock(direction):
    separator()
    print("  ADD STOCK" if direction == "in" else "  REMOVE STOCK")
    separator()
    produits = inv.list_products()
    if not produits:
        print("  No product available.")
        pause()
        return

    for p in produits:
        print(f"  {p}")

    try:
        pid    = prompt_str("Product ID")
        amount = prompt_int("Quantity", min_val=1)
        reason = prompt_str("Reason (optional)", required=False)

        if direction == "in":
            inv.add_stock_to_product(pid, amount, reason)
        else:
            inv.remove_stock_from_product(pid, amount, reason)

        log_message(f"Stock {'added' if direction == 'in' else 'removed'} : {pid} x{amount}", "info")
        print(f"\n  Stock updated successfully")
    except (KeyError, ValueError) as e:
        log_message(f"Error updating stock : {e}", "error")
        print(f"  Error : {e}")
    pause()


def archiver_produit():
    separator()
    produits = inv.list_products()
    if not produits:
        print("  No product.")
        pause()
        return

    for p in produits:
        print(f"  {p}")

    try:
        pid = prompt_str("Product ID to archive")
        inv.archive_product(pid)
        log_message(f"Product archived : {pid}", "info")
        print(f"  Product {pid} archived")
    except KeyError as e:
        log_message(f"Error archiving product : {e}", "error")
        print(f"  Error : {e}")
    pause()



#Customers
def menu_clients():
    while True:
        separator()
        print("  CUSTOMERS")
        separator()
        print("  1. List all customers")
        print("  2. Add a customer")
        print("  0. Back")
        separator()

        choix = input("Choice : ").strip()

        if choix == "1":
            lister_clients()
        elif choix == "2":
            ajouter_client()
        elif choix == "0":
            break
        else:
            print("  Invalid choice")


def lister_clients():
    separator()
    clients = inv.list_customers()
    if not clients:
        print("  No customers.")
        pause()
        return
    for c in clients:
        print(f"  {c}")
    pause()


def ajouter_client():
    separator()
    print("  NEW CUSTOMER")
    separator()
    try:
        name  = prompt_str("Name")
        email = prompt_str("Email")
        phone = prompt_str("Phone (optional)", required=False)

        c = inv.add_customer(name, email, phone)
        log_message(f"Customer created : {c.customer_id} - {c.name}", "info")
        print(f"\n  Customer created : {c}")
    except ValueError as e:
        log_message(f"Error creating customer : {e}", "error")
        print(f"  Error : {e}")
    pause()


#Orders
def menu_commandes():
    while True:
        separator()
        print("  ORDERS")
        separator()
        print("  1. List all orders")
        print("  2. Create an order")
        print("  3. Add a line to an order")
        print("  4. Confirm an order")
        print("  5. Mark as shipped")
        print("  6. Cancel an order")
        print("  0. Back")
        separator()

        choix = input("Choice : ").strip()

        if choix == "1":
            lister_commandes()
        elif choix == "2":
            creer_commande()
        elif choix == "3":
            ajouter_ligne()
        elif choix == "4":
            changer_statut_commande("confirm")
        elif choix == "5":
            changer_statut_commande("done")
        elif choix == "6":
            changer_statut_commande("cancel")
        elif choix == "0":
            break
        else:
            print("  Invalid choice")


def lister_commandes():
    separator()
    print("  Filter by status ? (empty = all)")
    statut = prompt_str("Status (draft / confirmed / done / cancelled)", required=False) or None
    orders = inv.list_orders(status=statut)
    if not orders:
        print("  No orders.")
        pause()
        return
    for o in orders:
        print(f"\n  {o}")
    pause()


def creer_commande():
    separator()
    clients = inv.list_customers()
    if not clients:
        print("  No customer available. First create a customer.")
        pause()
        return

    print("  AVAILABLE CUSTOMERS")
    for c in clients:
        print(f"  {c}")

    try:
        cid   = prompt_str("Customer ID")
        order = inv.create_order(cid)
        log_message(f"Order created : {order.order_id}", "info")
        print(f"\n  Order created : {order.order_id}")
    except KeyError as e:
        log_message(f"Error creating order : {e}", "error")
        print(f"  Error : {e}")
    pause()


def ajouter_ligne():
    separator()
    orders = inv.list_orders(status="draft")
    if not orders:
        print("  No order in draft.")
        pause()
        return

    print("  ORDERS IN DRAFT")
    for o in orders:
        print(f"  [{o.order_id}] {o.customer.name} — {len(o.lines)} line(s)")

    produits = inv.list_products()
    if not produits:
        print("  No products available.")
        pause()
        return

    try:
        oid     = prompt_str("Order ID")
        order   = inv.get_order(oid)

        print("\n  AVAILABLE PRODUCTS")
        for p in produits:
            print(f"  {p}")

        pid      = prompt_str("Product ID")
        product  = inv.get_product(pid)
        quantity = prompt_int("Quantity", min_val=1)

        order.add_line(product, quantity)
        inv.db.commit()     # persist the line addition via DB
        log_message(f"Line added to order {oid} : {pid} x{quantity}", "info")
        print(f"\n  Line added — Order total : {order.total:.2f}€")
    except (KeyError, ValueError, RuntimeError) as e:
        log_message(f"Error adding line : {e}", "error")
        print(f"  Error : {e}")
    pause()


def changer_statut_commande(action):
    separator()
    try:
        oid = prompt_str("Order ID")
        if action == "confirm":
            inv.confirm_order(oid)
            log_message(f"Order confirmed : {oid}", "info")
            print(f"  Order {oid} confirmed")
        elif action == "done":
            inv.mark_order_done(oid)
            log_message(f"Order marked as shipped : {oid}", "info")
            print(f"  Order {oid} marked as shipped")
        elif action == "cancel":
            inv.cancel_order(oid)
            log_message(f"Order cancelled : {oid}", "info")
            print(f"  Order {oid} cancelled")
    except (KeyError, RuntimeError) as e:
        log_message(f"Error updating order status : {e}", "error")
        print(f"  Error : {e}")
    pause()


#Reports
def menu_rapports():
    while True:
        separator()
        print("  REPORTS")
        separator()
        print("  1. Full stock report")
        print("  2. Products in low stock")
        print("  3. All orders")
        print("  4. Stock moves")
        print("  5. Export moves to CSV")
        print("  0. Back")
        separator()

        choix = input("Choice : ").strip()

        if choix == "1":
            inv.report_stock()
            pause()
        elif choix == "2":
            inv.report_low_stock()
            pause()
        elif choix == "3":
            inv.report_orders()
            pause()
        elif choix == "4":
            rapport_mouvements()
        elif choix == "5":
            exporter_csv()
        elif choix == "0":
            break
        else:
            print("  Invalid choice")


def rapport_mouvements():
    separator()
    if not inv.stock_moves:
        print("  No move saved.")
        pause()
        return
    for move in inv.stock_moves:
        print(f"  {move}")
    pause()


def exporter_csv():
    separator()
    filepath = prompt_str("Filename (def : export.csv)", required=False) or "export.csv"
    inv.export_csv(filepath)
    pause()



#Main menu
def menu_principal():
    while True:
        separator()
        print("  MANAGEMENT")
        separator()
        print("  1. Products")
        print("  2. Customers")
        print("  3. Orders")
        print("  4. Reports & Export")
        print("  0. Quit")
        separator()

        choix = input("Choice : ").strip()

        if choix == "1":
            menu_produits()
        elif choix == "2":
            menu_clients()
        elif choix == "3":
            menu_commandes()
        elif choix == "4":
            menu_rapports()
        elif choix == "0":
            inv.db.disconnect()
            log_message("App stopped", "info")
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid choice")


#==============================================

if __name__ == "__main__":
    log_message("Starting the app", "info")
    menu_principal()
