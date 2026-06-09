--PRODUCTS
INSERT INTO products(product_id,product_name,price,quantity,minimum_stock,category,active) VALUES('P1','Laptop Pro 15', 1299.99, 10, 3, 'Hardware', True);
INSERT INTO products(product_id,product_name,price,quantity,minimum_stock,category,active) VALUES('P2','Souris Ergonomique', 29.99, 50, 10, 'Hardware', True);
INSERT INTO products(product_id,product_name,price,quantity,minimum_stock,category,active) VALUES('P3','Bureau Standing', 349.99, 10, 2, 'Furniture', True);
INSERT INTO products(product_id,product_name,price,quantity,minimum_stock,category,active) VALUES('P4','Casque Audio', 89.99, 10, 5, 'Audio', True);
--CUSTOMERS
INSERT INTO customers(customer_id,customer_name,email,phone,active) VALUES('C1','John','John@example.com','04 000 00 00', True);
INSERT INTO customers(customer_id,customer_name,email,phone,active) VALUES('C2','Bob','bob@example.com','',True);
--ORDERS
INSERT INTO orders(order_id,customer_id,customer_name,order_status,created_at,total) VALUES('CMD/2026/0001','C1','John','draft',NOW(),0);
INSERT INTO orders(order_id,customer_id,customer_name,order_status,created_at,total) VALUES('CMD/2026/0002','C2','John','cancelled',NOW(),0);
--STOCK_MOVES
INSERT INTO stock_moves(product_id,product_name,quantity,direction,reason,created_at) VALUES('P4','Casque Audio',10,'in','restock',NOW());
