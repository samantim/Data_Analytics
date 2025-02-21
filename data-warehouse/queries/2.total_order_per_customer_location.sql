select 
	customers.city_id, cities.name as city_name, customers.zipcode,
	count(distinct orders.order_id) as total_orders,
    sum(order_details.price * order_details.quantity) as total_spent
from 
	order_details left join orders on order_details.order_id = orders.order_id
	left join customers on orders.customer_id = customers.customer_id
    left join cities on customers.city_id = cities.city_id
group by
	city_id, city_name, zipcode
order by 
	total_orders desc
