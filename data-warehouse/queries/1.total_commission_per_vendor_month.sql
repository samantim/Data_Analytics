select 
    vendors.vendor_id, vendors.name as vendor_name,
    SUM(order_details.price * order_details.quantity * vendors.commission_rate) AS total_commission
from 
	order_details left join orders on order_details.order_id = orders.order_id
	left join vendor_products on order_details.vendor_product_id = vendor_products.vendor_product_id
	left join vendors on vendor_products.vendor_id = vendors.vendor_id
where 
	DATE_FORMAT(orders.created_at, '%Y-%m') = '2025-01'
group by 
	vendor_id, vendor_name
order by 
	total_commission desc;
    