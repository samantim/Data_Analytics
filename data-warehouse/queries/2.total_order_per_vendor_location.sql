select 
	vendors.city_id, cities.name as city_name, vendors.zipcode,
	count(distinct orders.order_id) as total_orders,
    sum(order_details.price * order_details.quantity) as total_spent
from 
	order_details left join orders on order_details.order_id = orders.order_id
    left join vendor_products on order_details.vendor_product_id = vendor_products.vendor_product_id
	left join vendors on vendor_products.vendor_id = vendors.vendor_id
    left join cities on vendors.city_id = cities.city_id
group by
	city_id, city_name, zipcode
order by 
	total_orders desc
    