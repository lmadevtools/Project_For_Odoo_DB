"""
main.py — Demo script showcasing all major features of the inventory system
Logs are written to logs/app.log in parallel
"""

from Classes.inventory import Inventory
from Utils.helper import log_message


def separator(title=""):
    line = "=" * 60
    if title:
        print(f"\n{line}")
        print(f"  {title}")
        print(line)
    else:
        print(line)


def section(title):
    separator(title)
    log_message(f"--- {title} ---", "info")



#Products
def demo_products(inv):
    section("PRODUCTS — Creation")

    computer  = inv.add_product("Computer", 1299.99, 10, minimum_stock=3, category="IT")
    mouse   = inv.add_product("Mouse", 29.99, 50, minimum_stock=10, category="IT")
    desk    = inv.add_product("Desk", 349.99, 4, minimum_stock=2, category="Furniture")
    keyboard = inv.add_product("Keyboard", 89.99, 3, minimum_stock=5, category="Others")

    log_message(f"4 products created", "info")

    for p in inv.list_products():
        print(f"  {p}")

    section("PRODUCTS — Stock management")

    inv.add_stock_to_product(computer.product_id,  5, reason="Restock")
    inv.add_stock_to_product(keyboard.product_id, 10, reason="Delivery")
    inv.remove_stock_from_product(mouse.product_id, 3, reason="Others Use")

    print("  After stock updates :")
    for p in inv.list_products():
        print(f"  {p}")

    section("PRODUCTS — Low stock report")

    low = inv.list_low_stock()
    if low:
        for p in low:
            print(f"  ⚠  {p}")
            log_message(f"Low stock : {p.name} ({p.quantity} units)", "warning")
    else:
        print("  No low stock products.")

    section("PRODUCTS — Archive")

    inv.archive_product(desk.product_id)
    print(f"  Desk archived.")
    log_message(f"Product archived : {desk.product_id}", "info")

    print(f"  Active products    : {len(inv.list_products())}")
    print(f"  All products       : {len(inv.list_products(include_archived=True))}")

    return computer, mouse, keyboard


#Customers
def demo_customers(inv):
    section("CUSTOMERS — Creation")

    jeanne = inv.add_customer("Jeanne O",  "Jeanne@example.com", "0494 00 00 00")
    benoit = inv.add_customer("Benoit B",    "Benoit@example.com")
    johnny = inv.add_customer("Johnny L", "Johnny@example.com", "0498 00 00 00")

    log_message("3 customers created", "info")

    for c in inv.list_customers():
        print(f"  {c}")

    section("CUSTOMERS — Archive")

    johnny.archive()
    print(f"  Johnny archived.")
    print(f"  Active customers : {len(inv.list_customers())}")
    print(f"  All customers    : {len(inv.list_customers(include_archived=True))}")
    log_message(f"Customer archived : {johnny.customer_id}", "info")

    return jeanne, benoit


#Orders
def demo_orders(inv, computer, mouse, keyboard, jeanne, benoit):
    section("ORDERS — Jeanne : draft → confirmed → done")

    order1 = inv.create_order(jeanne.customer_id)
    print(f"  Order created : {order1.order_id}")
    log_message(f"Order created : {order1.order_id}", "info")

    order1.add_line(inv.get_product(computer.product_id),  1)
    order1.add_line(inv.get_product(mouse.product_id),   2)
    inv.db.commit()
    print(f"  Lines added — total : {order1.total:.2f}€")
    print(f"  {order1}")

    inv.confirm_order(order1.order_id)
    print(f"\n  → Confirmed. Stock updated.")
    print(f"  computer stock : {inv.get_product(computer.product_id).quantity}")
    print(f"  Mouse stock  : {inv.get_product(mouse.product_id).quantity}")
    log_message(f"Order confirmed : {order1.order_id}", "info")

    inv.mark_order_done(order1.order_id)
    print(f"  → Marked as done.")
    log_message(f"Order done : {order1.order_id}", "info")

    section("ORDERS — Benoit : draft → confirmed → cancelled")

    order2 = inv.create_order(benoit.customer_id)
    print(f"  Order created : {order2.order_id}")
    log_message(f"Order created : {order2.order_id}", "info")

    order2.add_line(inv.get_product(keyboard.product_id), 2)
    inv.db.commit()
    print(f"  Lines added — total : {order2.total:.2f}€")

    inv.confirm_order(order2.order_id)
    print(f"  → Confirmed. keyboard stock : {inv.get_product(keyboard.product_id).quantity}")

    inv.cancel_order(order2.order_id)
    print(f"  → Cancelled. keyboard stock restored : {inv.get_product(keyboard.product_id).quantity}")
    log_message(f"Order cancelled : {order2.order_id}", "info")

    section("ORDERS — Draft cancelled without stock impact")

    order3 = inv.create_order(jeanne.customer_id)
    order3.add_line(inv.get_product(mouse.product_id), 5)
    inv.db.commit()
    stock_before = inv.get_product(mouse.product_id).quantity
    inv.cancel_order(order3.order_id)
    stock_after  = inv.get_product(mouse.product_id).quantity
    print(f"  Draft cancelled — mouse stock unchanged : {stock_before} → {stock_after}")
    log_message(f"Draft order cancelled : {order3.order_id}", "info")

    section("ORDERS — List by status")

    for status in ("draft", "confirmed", "done", "cancelled"):
        orders = inv.list_orders(status=status)
        print(f"  {status.upper():<12} : {len(orders)} order(s)")


#Stock moves
def demo_stock_moves(inv):
    section("STOCK MOVES — History")

    if not inv.stock_moves:
        print("  No moves recorded.")
        return

    print(f"  {len(inv.stock_moves)} move(s) recorded :\n")
    for move in inv.stock_moves:
        print(f"  {move}")

    section("STOCK MOVES — CSV Export")

    inv.export_csv("demo_export.csv")
    log_message("CSV exported : demo_export.csv", "info")


#Summary
def demo_summary(inv):
    section("SUMMARY")
    print(repr(inv))
    log_message("Demo completed successfully", "info")


#Main
def main():
    log_message("=== Demo starting ===", "info")
    separator("INVENTORY MANAGEMENT SYSTEM — DEMO")

    inv = Inventory()

    try:
        computer, mouse, keyboard = demo_products(inv)
        jeanne, benoit             = demo_customers(inv)
        demo_orders(inv, computer, mouse, keyboard, jeanne, benoit)
        demo_stock_moves(inv)
        demo_summary(inv)

    except Exception as e:
        log_message(f"Unexpected error : {e}", "error")
        print(f"\n  ERROR : {e}")
        raise

    finally:
        inv.db.disconnect()
        log_message("=== Demo ended ===", "info")
        separator()


if __name__ == "__main__":
    main()
