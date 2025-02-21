(select 
	customers.city_id, cities.name as city_name
from 
	order_details left join orders on order_details.order_id = orders.order_id
	left join customers on orders.customer_id = customers.customer_id
    left join cities on customers.city_id = cities.city_id
group by
	city_id, city_name
order by 
	count(distinct orders.order_id) desc
limit 20)
intersect
(select 
	vendors.city_id, cities.name as city_name
from 
	order_details left join orders on order_details.order_id = orders.order_id
    left join vendor_products on order_details.vendor_product_id = vendor_products.vendor_product_id
	left join vendors on vendor_products.vendor_id = vendors.vendor_id
    left join cities on vendors.city_id = cities.city_id
group by
	city_id, city_name
order by 
	count(distinct orders.order_id) desc
limit 20)
