-- Task3:  Write a query to find the 𝐩𝐞𝐫𝐜𝐞𝐧𝐭𝐚𝐠𝐞 𝐨𝐟 𝐮𝐬𝐞𝐫𝐬 𝐟𝐫𝐨𝐦 𝐞𝐚𝐜𝐡 𝐜𝐨𝐮𝐧𝐭𝐫𝐲 who made 𝐚𝐭 𝐥𝐞𝐚𝐬𝐭 𝐨𝐧𝐞 𝐭𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧 𝐰𝐢𝐭𝐡𝐢𝐧 𝟑𝟎 𝐝𝐚𝐲𝐬 𝐨𝐟 𝐬𝐢𝐠𝐧𝐢𝐧𝐠 𝐮𝐩.
with users_has_tx30 as (
	select users.user_id as user_id, users.country as country
	from transactions left join users on transactions.user_id = users.user_id
	where transaction_date between signup_date and adddate(signup_date, interval 30 day)
) -- CTE to fetch 𝐮𝐬𝐞𝐫𝐬 who made 𝐚𝐭 𝐥𝐞𝐚𝐬𝐭 𝐨𝐧𝐞 𝐭𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧 𝐰𝐢𝐭𝐡𝐢𝐧 𝟑𝟎 𝐝𝐚𝐲𝐬 𝐨𝐟 𝐬𝐢𝐠𝐧𝐢𝐧𝐠 𝐮𝐩
select 
	users.country, round(100 * (select count(user_id) from users_has_tx30 where country = users.country) / count(users.user_id),2)
from 
	users
group by 
	users.country;
