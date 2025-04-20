-- Task1: Write a query to identify users who had 𝐦𝐨𝐫𝐞 𝐭𝐡𝐚𝐧 𝟑 𝐅𝐑𝐀𝐔𝐃𝐔𝐋𝐄𝐍𝐓 𝐭𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧𝐬 𝐢𝐧 𝐭𝐡𝐞 𝐥𝐚𝐬𝐭 𝟑𝟎 𝐝𝐚𝐲𝐬.
select 
	user_id, count(transaction_id) as fraudulent_tx_count
from 
	transactions
where 
	transaction_status = 'fraudulent' and transaction_date between subdate(current_date(), interval 30 day) and current_date()
group by 
	user_id
having 
	fraudulent_tx_count > 3;