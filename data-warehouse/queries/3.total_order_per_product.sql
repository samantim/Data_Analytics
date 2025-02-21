select 
	products.product_id, products.name as product_name,
	count(order_details.order_detail_id) as total_orders,
    (select count(vendor_id) from vendor_products as v_p where v_p.product_id = products.product_id) as vendor_count
from 
	order_details left join vendor_products on order_details.vendor_product_id = vendor_products.vendor_product_id
	left join products on vendor_products.product_id = products.product_id
group by
	product_id, product_name
order by 
	total_orders desc
    