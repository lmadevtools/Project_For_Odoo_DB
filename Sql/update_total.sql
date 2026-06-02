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
WHERE O.order_id = agg.order_id







