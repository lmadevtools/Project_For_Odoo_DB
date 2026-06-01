from Utils.helper import log_message
from Classes.inventory import Inventory

def main():
    log_message("Starting the app","info")    
    inv = Inventory("data_products.json","data_customers.json","data_orders.json","data_stock_moves.json")

    # Products
    print("Test adding products")
    laptop  = inv.add_product("Laptop Pro 15", 1299.99, 10, minimum_stock=3, category="Hardware")
    mouse   = inv.add_product("Souris Ergonomique", 29.99, 50, minimum_stock=10, category="Hardware")
    desk    = inv.add_product("Bureau Standing", 349.99,  4, minimum_stock=2, category="Furniture")
    headset = inv.add_product("Casque Audio", 89.99,  3, minimum_stock=5, category="Audio")

    inv.report_stock()

    # Clients
    print("Test adding clients")
    try:
        john = inv.add_customer("John", "John@example.com",  "04 000 00 00")
        print(john)
        bob  = inv.add_customer("Bob",  "bob@example.com")
        print(bob)
    except (ValueError) as e:    
        log_message("e","error")

    # Orders
    #john order then valid
    print("\nJohn command")
    try:
        order1 = inv.create_order(john.customer_id)
        order1.add_line(inv.get_product(laptop.product_id), 1)
        order1.add_line(inv.get_product(mouse.product_id),  2)
        inv._save()

        print(order1)
    except (ValueError) as e:    
        log_message("e","error")
    else:
        print("\nOrder confirmation...")
        try:
            inv.confirm_order(order1.order_id)
        except (RuntimeError) as e:    
            log_message("e","error")
        else:
            print(order1)

    # Bob order then cancel
    try:
        print("\nBob command")
        order2 = inv.create_order(bob.customer_id)
        order2.add_line(inv.get_product(headset.product_id), 3)
        order2.add_line(inv.get_product(desk.product_id),    2)
        inv._save()

        print(order2)
    except (ValueError) as e:    
        log_message("e","error")
    else:
        print("\nCancel order")
        try:
            inv.cancel_order(order2.order_id)
        except (RuntimeError) as e:    
            log_message("e","error")
        else:
            print(f"Statut : {order2.status}")

    # 5. report low stock
    inv.report_low_stock()

    # 6. report orders
    inv.report_orders()

    #7. stock_move
    move = inv.add_stock_to_product(laptop.product_id, 10, "Recept")
    inv._save()
    print(move)
    move = inv.remove_stock_from_product(mouse.product_id, 3, "Sold")
    inv._save()
    print(move)
    print()

    #8. export to csv
    inv.export_csv("data_stock_moves.csv")
    print(inv)
    print()

    log_message("Ending the app","info")

if __name__ == "__main__":
    main()
