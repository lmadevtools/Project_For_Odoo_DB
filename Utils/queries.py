#PRODUCTS
CREATE_PRODUCT      =   "INSERT INTO products (product_id, product_name, price, quantity, minimum_stock, category, active) VALUES (%s,%s,%s,%s,%s,%s,%s)"
GET_PRODUCT         =   "SELECT * FROM products WHERE product_id = %s"
LIST_PRODUCTS       =   "SELECT * FROM products WHERE active = TRUE"
UPDATE_PRODUCT      =   "UPDATE products SET product_name =%s, price=%s, quantity=%s WHERE product_id=%s"
ARCHIVE_PRODUCT     =   "UPDATE products SET active = FALSE WHERE product_id = %s"
UNARCHIVE_PRODUCT   =   "UPDATE products SET active = TRUE WHERE product_id = %s"

#CUSTOMERS
CREATE_CUSTOMER     =  "INSERT INTO customers(customer_id,customer_name,email,phone,active) VALUES (%s,%s,%s,%s,%s)"   
GET_CUSTOMERS       =  "SELECT * FROM customers WHERE customer_id = %s"
LIST_CUSTOMERS      =  "SELECT * FROM customers WHERE active = TRUE"
ARCHIVE_CUSTOMER    =  "UPDATE customers SET active = FALSE WHERE customer_id = %s"
UNARCHIVE_CUSTOMER  =  "UPDATE customers SET active = TRUE WHERE customer_id = %s"

#ORDERS
CREATE_ORDER        =   "INSERT INTO orders(order_id,customer_id,customer_name,order_status,created_at) VALUES(%s,%s,%s,%s,%s)"
GET_ORDER           =   "SELECT * FROM orders WHERE order_id = %s"
UPDATE_ORDER        =   'UPDATE orders SET order_status = %s WHERE order_id = %s'
LIST_ORDERS         =   "SELECT * FROM orders"

#ORDER_LINES         
ADD_ORDER_LINES     =   "INSERT INTO order_lines(order_id, product_id, product_name, quantity, unit_price, subtotal) VALUES (%s,%s,%s,%s,%s,%s)"
LIST_ORDER_LINES    =   "SELECT * FROM order_lines WHERE order_id = %s"   

#STOCK_MOVES
INSERT_STOCK_MOVES  =   "INSERT INTO stock_moves (product_id, product_name, quantity, direction, reason, created_at) VALUES (%s,%s,%s,%s,%s,%s)"
LIST_STOCK_MOVES    =   "SELECT * FROM stock_moves ORDER BY created_at DESC"
