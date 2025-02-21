select 
	categories.category_id, categories.name as category_name,
	count(order_details.order_detail_id) as total_orders,
	sum(order_details.price * order_details.quantity) as total_spent
from 
	order_details left join vendor_products on order_details.vendor_product_id = vendor_products.vendor_product_id
	left join products on vendor_products.product_id = products.product_id
	left join categories on products.category_id = categories.category_id
group by
	category_id, category_name
order by 
	total_orders desc
    