select distinct
	products.product_id, products.name as product_name, quarter(orders.created_at) as year_quarter,
    count(order_details.order_detail_id) over (partition by products.product_id order by quarter(orders.created_at)) as total_orders
from 
	order_details left join orders on order_details.order_id = orders.order_id
    left join vendor_products on order_details.vendor_product_id = vendor_products.vendor_product_id
	left join products on vendor_products.product_id = products.product_id
order by 
	year_quarter, total_orders desc, product_id
