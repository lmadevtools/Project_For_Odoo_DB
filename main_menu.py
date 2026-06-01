from Utils.helper import log_message
from Classes.inventory import Inventory

inv = Inventory()

#add a separator line
def separator():
    print("\n" + "=" * 50)

#wait user to push Enter
def pause():
    input("\nEnter to continue")

#waiting integer 
def prompt_int(label, min_val=None):
    while True:
        try:
            val = int(input(f"{label} : "))
            if min_val is not None and val < min_val:
                print(f" minimum value : {min_val}")
                continue
            return val
        except ValueError:
            print(" integer awaited")

#waiting float
def prompt_float(label, min_val=None):
    while True:
        try:
            val = float(input(f"{label} : "))
            if min_val is not None and val < min_val:
                print(f" minimum value : {min_val}")
                continue
            return val
        except ValueError:
            print(" integer number awaited")

#waiting string
def prompt_str(label, required=True):
    while True:
        val = input(f"{label} : ").strip()
        if required and not val:
            print(" mandatory field")
            continue
        return val

#display list of options and return the user choice
def choose(options: list, label="Choice") -> str:
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            idx = int(input(f"{label} : "))
            if 1 <= idx <= len(options):
                return options[idx - 1]
            print(f" between 1 and {len(options)}")
        except ValueError:
            print(" integer number awaited")


##########PRODUCTS###########
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
            print("Invalid choice")


def lister_produits():
    separator()
    produits = inv.list_products()
    if not produits:
        print("  no product.")
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
        minimum_stock = prompt_int("minimum stock", min_val=0)
        category      = prompt_str("Category (def : General)", required=False) or "General"

        p = inv.add_product(name, price, quantity, minimum_stock, category)
        print(f"\n  Product created : {p}")
    except ValueError as e:
        print(f" Error : {e}")
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

        print(f"\n Stock updated successfully")
    except (KeyError, ValueError) as e:
        print(f" Error : {e}")
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
        pid = prompt_str("product ID to archive")
        inv.archive_product(pid)
        print(f" Product {pid} archived")
    except KeyError as e:
        print(f" Error : {e}")
    pause()


##########CUSTOMERS###########
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
            print("Invalid choice")


def lister_clients():
    separator()
    clients = inv.list_customers()
    if not clients:
        print("  No customers")
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
        phone = prompt_str("Phone (optionnal)", required=False)

        c = inv.add_customer(name, email, phone)
        print(f"\n Customer created : {c}")
    except ValueError as e:
        print(f" Error : {e}")
    pause()


##########ORDERS###########
def menu_commandes():
    while True:
        separator()
        print("  ORDERS")
        separator()
        print("  1. List all orders")
        print("  2. Crate an order")
        print("  3. Add a row to an order")
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
            print("Invalid choice")


def lister_commandes():
    separator()
    print("  Filter per status ? (empty = all)")
    statut = prompt_str("Status (draft / confirmed / done / cancelled)", required=False) or None
    orders = inv.list_orders(status=statut)
    if not orders:
        print("  no orders")
        pause()
        return
    for o in orders:
        print(f"\n  {o}")
    pause()


def creer_commande():
    separator()
    clients = inv.list_customers()
    if not clients:
        print("  no customer available. First create a customer.")
        pause()
        return

    print("AVAILABLE CUSTOMERS")
    for c in clients:
        print(f"  {c}")

    try:
        cid   = prompt_str("customer ID")
        order = inv.create_order(cid)
        print(f"\n order created : {order.order_id}")
    except KeyError as e:
        print(f" Error : {e}")
    pause()


def ajouter_ligne():
    separator()
    orders = inv.list_orders(status="draft")
    if not orders:
        print("  No order in draft.")
        pause()
        return

    print("  ORDER IN DRAFT")
    for o in orders:
        print(f"  [{o.order_id}] {o.customer.name} — {len(o.lines)} ligne(s)")

    produits = inv.list_products()
    if not produits:
        print("  No products available.")
        pause()
        return

    try:
        oid      = prompt_str("order ID")
        order    = inv.get_order(oid)

        print("\n AVAILABLE PRODUCTS")
        for p in produits:
            print(f"  {p}")

        pid      = prompt_str("product ID")
        product  = inv.get_product(pid)
        quantity = prompt_int("Quantity", min_val=1)

        order.add_line(product, quantity)
        inv._save()
        print(f"\n  row added — Total order : {order.total:.2f}€")
    except (KeyError, ValueError, RuntimeError) as e:
        print(f" Error : {e}")
    pause()


def changer_statut_commande(action):
    separator()
    try:
        oid = prompt_str("order ID")
        if action == "confirm":
            inv.confirm_order(oid)
            print(f" order {oid} confirmed")
        elif action == "done":
            inv.mark_order_done(oid)
            print(f" order {oid} marked as shipped")
        elif action == "cancel":
            inv.cancel_order(oid)
            print(f" order {oid} canceled")
    except (KeyError, RuntimeError) as e:
        print(f" Error : {e}")
    pause()


#########REPORTS#########
def menu_rapports():
    while True:
        separator()
        print("  REPORTS")
        separator()
        print("  1. REPORT full stock")
        print("  2. Product in low stock")   
        print("  3. All orders")
        print("  4. Stock moves")
        print("  5. Export move to CSV")
        print("  0. Back")
        separator()
        #we should add a possibility to order a list of low stock item,
        #automatically, per mail, to the supplier

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
            print("Invalid Choice")


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


##########MENU#########
def menu_principal():
    while True:
        separator()
        print("MANAGEMENT")
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
            break
        else:
            print(" Invalid choice")


# ======================================================================

if __name__ == "__main__":
    log_message("Starting the app","info")
    menu_principal()
    log_message("Ending the app","info")