DELIMITER //

CREATE PROCEDURE monthly_report(IN report_month VARCHAR(7))
BEGIN
select 
	SUM(order_details.price * order_details.quantity ) AS total_order,
    SUM(order_details.price * order_details.quantity * vendors.commission_rate) AS total_commission,
    (select ifnull(sum(order_statuses.cost), 0) from order_statuses where order_statuses.order_id in (
    SELECT DISTINCT orders.order_id 
                FROM orders 
                WHERE DATE_FORMAT(orders.created_at, '%Y-%m') = report_month)) as total_cost,
    SUM(order_details.price * order_details.quantity * vendors.commission_rate) -
    (select ifnull(sum(order_statuses.cost), 0) from order_statuses where order_statuses.order_id in (
    SELECT DISTINCT orders.order_id 
                FROM orders 
                WHERE DATE_FORMAT(orders.created_at, '%Y-%m') = report_month)) as profit
from 
	order_details left join orders on order_details.order_id = orders.order_id
	left join vendor_products on order_details.vendor_product_id = vendor_products.vendor_product_id
	left join vendors on vendor_products.vendor_id = vendors.vendor_id
WHERE 
	DATE_FORMAT(orders.created_at, '%Y-%m') = report_month;
END; //

DELIMITER ;

