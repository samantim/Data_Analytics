select 
	case when customers.is_member = 1 then 'member' else 'guest' end as membership,
	count(order_details.order_detail_id) as total_orders,
	sum(order_details.price * order_details.quantity) as total_spent
from 
	order_details left join orders on order_details.order_id = orders.order_id
	left join customers on orders.customer_id = customers.customer_id
group by
	membership
order by 
	total_orders desc
    