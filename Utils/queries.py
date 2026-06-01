#PRODUCTS
CREATE_PRODUCT      =   "INSERT INTO products (product_id, name, price, quantity, minimum_stock, category, active) VALUES (%s,%s,%s,%s,%s,%s,%s)"
GET_PRODUCT         =   "SELECT * FROM products WHERE product_id = %s"
LIST_PRODUCTS       =   "SELECT * FROM products WHERE active = TRUE"
UPDATE_PRODUCT      =   "UPDATE products SET name =%s, price=%s, quantity=%s WHERE product_id=%s"
ARCHIVE_PRODUCT     =   "UPDATE products SET active = FALSE WHERE product_id = %s"

#CUSTOMERS
CREATE_CUSTOMER     =  "INSERT INTO customers(customer_id,name,email,phone,active) VALUES (%s,%s;%s,%s,%s)"   
GET_CUSTOMERS       =  "SELECT * FROM customers WHERE customer_id = %s"

#ORDERS
CREATE_ORDER        =   "INSERT INTO orders(order_id,customer_id,status,created_at) VALUES(%s,%s,%s,%s)"
GET_ORDER           =   "SELECT * FROM orders WHERE order_is = %s"
UPDATE_ORDER        =   'UPDATE orders SET status = %s WHERE order_id = %s'

#STOCK_MOVES
INSERT_STOCK_MOVES  =   "INSERT INTO stock_moves (product_id, product_name, quantity, direction, reason, created_at) VALUES (%s,%s,%s,%s;%s,%s)"
LIST_STOCK_MOVES    =   "SELECT * FROM stock_moves ORDER BY created_at DESC"
