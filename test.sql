INSERT INTO sales_db.product_schema.product_info_table (product_name, product_price)
SELECT 
    CONCAT(p.product_name, ' - ', c.category_name) AS product_name,
    (p.product_cost * 1.2) AS product_price
FROM 
    sales_db.product_schema.product_table p
JOIN 
    sales_db.category_schema.category_table c 
ON 
    p.category_id = c.category_id;
