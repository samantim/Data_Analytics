-- Task5: Write a query to calculate the 𝐌𝐨𝐧𝐭𝐡𝐥𝐲 𝐑𝐞𝐜𝐮𝐫𝐫𝐢𝐧𝐠 𝐑𝐞𝐯𝐞𝐧𝐮𝐞 (𝐌𝐑𝐑) for each month over the 𝐥𝐚𝐬𝐭 𝐲𝐞𝐚𝐫.
-- consider if today is 20-04-2025 -->  𝐥𝐚𝐬𝐭 𝐲𝐞𝐚𝐫 : 01-01-2024 to 31-12-2024
-- the subscription fees in the table are assumed to be monthly
set @lastyear_start = makedate(year(subdate(current_date(), interval 1 year)), 1);
set @lastyear_end = last_day(adddate(makedate(year(subdate(current_date(), interval 1 year)), 1), interval 11 month));

with months as (
select 1 as gen_month union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9 union select 10 union select 11 union select 12
),
effective_subscriptions as (
select 
	case when subscription_start_date > @lastyear_start then subscription_start_date else @lastyear_start end effective_start_date,
    case when subscription_end_date < @lastyear_end then subscription_end_date else @lastyear_end end effective_end_date,
    subscription_amount
from subscriptions
where
	(subscription_start_date between @lastyear_start and @lastyear_end)
or
	(subscription_start_date < @lastyear_start and subscription_end_date > @lastyear_start)
)
select 
	gen_month, round(sum(subscription_amount),2)
from 
	months left join effective_subscriptions on months.gen_month between month(effective_start_date) and month(effective_end_date)
group by 
	gen_month;
