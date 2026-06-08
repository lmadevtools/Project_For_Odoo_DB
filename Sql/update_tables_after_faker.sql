--update unit_price in orderlines to get the correct price from product
UPDATE order_lines OL
SET unit_price = agg.price
FROM ( 
    SELECT product_id, price
    FROM products P
) agg 
WHERE OL.product_id = agg.product_id;

--order lines subtotal recalculate
UPDATE order_lines SET subtotal = quantity * unit_price WHERE 1=1;

--orders total reset to 0
UPDATE orders SET total = 0 WHERE 1=1;

--orders total recalculate
UPDATE orders O
SET total = agg.total_amount
FROM ( 
    SELECT order_id, SUM(subtotal) AS total_amount
    FROM order_lines OL
    GROUP BY order_id
) agg 
WHERE O.order_id = agg.order_id;

--update customer name in order to get the correct name from customers
UPDATE orders O
SET customer_name = agg.customer_name
FROM ( 
    SELECT customer_id, customer_name
    FROM customers C
) agg 
WHERE O.customer_id = agg.customer_id;

--update product name in orderlines to get the correct name from products
UPDATE order_lines OL
SET product_name = agg.product_name
FROM ( 
    SELECT product_id, product_name
    FROM products P
) agg 
WHERE OL.product_id = agg.product_id;

--update product name in stock move to get the correct name from products
UPDATE stock_moves SM
SET product_name = agg.product_name
FROM ( 
    SELECT product_id, product_name
    FROM products P
) agg 
WHERE SM.product_id = agg.product_id;







