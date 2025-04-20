-- Task4: Write a query to calculate the 𝐩𝐞𝐫𝐜𝐞𝐧𝐭𝐚𝐠𝐞 𝐨𝐟 𝐭𝐨𝐭𝐚𝐥 𝐭𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧 𝐯𝐨𝐥𝐮𝐦𝐞 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐞𝐝 𝐯𝐢𝐚 𝐏𝐚𝐲𝐏𝐚𝐥 over the 𝐥𝐚𝐬𝐭 𝐲𝐞𝐚𝐫.
-- consider if today is 20-04-2025 -->  𝐥𝐚𝐬𝐭 𝐲𝐞𝐚𝐫 : 01-01-2024 to 31-12-2024
select
	round(100 * sum(case when payment_method = 'paypal' then transaction_amount else 0 end)/ sum(transaction_amount), 2) as tx_percentage
from 
	transactions
where -- where clause provides all transactions over the 𝐥𝐚𝐬𝐭 𝐲𝐞𝐚𝐫
	transaction_date between makedate(year(subdate(current_date(), interval 1 year)), 1)
and
	last_day(adddate(makedate(year(subdate(current_date(), interval 1 year)), 1), interval 11 month));

-- Task4 bonus version "If you need all percentages, not only for the 'paypal'
-- you can uncomment the where clause if you want to have conditions
with tx_percentages_lastyear as
(
	select distinct payment_method, round(100 * sum(transaction_amount) over (partition by payment_method) / sum(transaction_amount) over (), 2) as tx_percentage
	from transactions
	where -- where clause provides all transactions over the 𝐥𝐚𝐬𝐭 𝐲𝐞𝐚𝐫
	transaction_date between makedate(year(subdate(current_date(), interval 1 year)), 1)
	and
	last_day(adddate(makedate(year(subdate(current_date(), interval 1 year)), 1), interval 11 month))
) -- the 𝐩𝐞𝐫𝐜𝐞𝐧𝐭𝐚𝐠𝐞 𝐨𝐟 𝐭𝐨𝐭𝐚𝐥 𝐭𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧 𝐯𝐨𝐥𝐮𝐦𝐞 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐞𝐝 over the 𝐥𝐚𝐬𝐭 𝐲𝐞𝐚𝐫 for all payment_methods
select 
	tx_percentage 
from 
	tx_percentages_lastyear
-- where 
-- 	payment_method = 'paypal'
;
