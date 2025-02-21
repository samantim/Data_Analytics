drop database if exists ecommerce;

create database ecommerce;

use ecommerce;

create table categories (
	category_id smallint not null auto_increment,
    name varchar(20) not null,
    created_at timestamp not null default current_timestamp,
    primary key (category_id),
    constraint category_name_unique unique (name)
);

create table statuses (
	status_id tinyint not null auto_increment,
    name varchar(20) not null,
    created_at timestamp not null default current_timestamp,
    primary key (status_id),
    constraint status_name_unique unique (name)
);

create table cities (
	city_id mediumint not null auto_increment,
    name varchar(50) not null,
    created_at timestamp not null default current_timestamp,
    primary key (city_id),
    constraint city_name_unique unique (name)
);

create table products (
	product_id int not null auto_increment,
    name varchar(100) not null,
    details varchar(1000),
    category_id smallint not null,
    image_url varchar(500),
    created_at timestamp not null default current_timestamp,
    primary key (product_id),
	foreign key (category_id) references categories(category_id) on delete restrict,
    constraint product_name_unique unique (name)
);
create index idx_products_category on products(category_id);
create index idx_products_name on products(name);

create table customers (
	customer_id int not null auto_increment,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    phone_number varchar(20) not null,
    street varchar(100) not null,
    house_number varchar(50) not null,
    zipcode mediumint not null,
    city_id mediumint not null,
    is_member bool not null default False,
    email varchar(200),
    created_at timestamp not null default current_timestamp,
    primary key (customer_id),
    foreign key (city_id) references cities(city_id) on delete restrict,
    constraint customer_phone_number_unique unique (phone_number),
    constraint customer_email_unique unique (email),
    check (zipcode > 0 and char_length(cast(zipcode as char)) = 5)
);
create index idx_customers_city on customers(city_id);
create index idx_customers_email on customers(email);

create table vendors (
	vendor_id int not null auto_increment,
    name varchar(200) not null,
    phone_number varchar(20) not null,
    street varchar(100) not null,
    house_number varchar(50) not null,
    zipcode mediumint not null,
    city_id mediumint not null,
    commission_rate decimal(2,2) not null,
    created_at timestamp not null default current_timestamp,
    primary key (vendor_id),
	foreign key (city_id) references cities(city_id) on delete restrict,
    constraint vendor_name_unique unique (name),
    constraint vendor_phone_number_unique unique (phone_number),
    check (zipcode > 0 and char_length(cast(zipcode as char)) = 5),
    check (commission_rate between 0 and 1)	
);
create index idx_vendors_city on vendors(city_id);

create table vendor_products (
	vendor_product_id bigint not null auto_increment,
    vendor_id int not null,
    product_id int not null,
    price decimal(9,2) not null,
    created_at timestamp not null default current_timestamp,
    primary key (vendor_product_id),
    foreign key (vendor_id) references vendors(vendor_id) on delete restrict,
    foreign key (product_id) references products(product_id) on delete restrict,
    constraint vendor_product_unique unique (vendor_id, product_id),
    check (price > 0)
);
create index idx_vendor_products_product on vendor_products(product_id);

create table orders (
	order_id bigint not null auto_increment,
    customer_id int not null,
    total_cost decimal(10,2) not null,
    created_at timestamp not null default current_timestamp,
    primary key (order_id),
    foreign key (customer_id) references customers(customer_id) on delete restrict,
    check (total_cost >= 0)
);
create index idx_orders_customer on orders(customer_id);

create table order_details (
	order_detail_id bigint not null auto_increment,
    order_id bigint not null,
    vendor_product_id bigint not null,
	quantity smallint not null,
    price decimal(9,2) not null,
    created_at timestamp not null default current_timestamp,
    primary key (order_detail_id),
    foreign key (order_id) references orders(order_id) on delete cascade,
    foreign key (vendor_product_id) references vendor_products(vendor_product_id) on delete restrict,
    constraint vender_product_order_unique unique (order_id, vendor_product_id),
    check (price > 0),
    check (quantity > 0)
);
create index idx_order_details_order on order_details(order_id);

create table order_statuses (
	order_status_id bigint not null auto_increment,
    order_id bigint not null,
    status_id tinyint not null,
	cost decimal(9,2) not null,
    created_at timestamp not null default current_timestamp,
    primary key (order_status_id),
    foreign key (order_id) references orders(order_id) on delete cascade,
    foreign key (status_id) references statuses(status_id) on delete restrict,
    constraint order_status_unique unique (order_id, status_id),
    check (cost >= 0)
);
create index idx_order_status_order on order_statuses(order_id);

create table reviews (
	review_id bigint not null auto_increment,
    customer_id int not null,
    vendor_product_id bigint not null,
	description varchar(1000),
    rating tinyint not null,
    created_at timestamp not null default current_timestamp,
    primary key (review_id),
    foreign key (customer_id) references customers(customer_id) on delete cascade,
    foreign key (vendor_product_id) references vendor_products(vendor_product_id) on delete cascade,
    constraint unique_customer_vendor_product unique (customer_id, vendor_product_id),
    check (rating between 1 and 5)
);
create index idx_reviews_vendor_product on reviews(vendor_product_id);

create table sessions (
	session_id bigint not null auto_increment,
    customer_id int not null,
    start_at timestamp not null default current_timestamp,
    end_at timestamp,
    primary key (session_id),
    foreign key (customer_id) references customers(customer_id) on delete cascade,
    check (end_at is null or end_at >= start_at)
);
create index idx_sessions_customer on sessions(customer_id);




-- triggers
-- change the delimiter to avoid conflicts with inner semicolons
delimiter //

create trigger before_review_insert
before insert on reviews for each row
begin
	if new.rating < 1 then 
		set new.rating = 1;
	elseif new.rating > 5 then
		set new.rating = 5;
	end if;
end;//

create trigger before_product_insert
before insert on products for each row
begin
	if ifnull(new.image_url,'') = '' then
		set new.image_url = "no_image.png";
	end if;
end;//

-- Reset the delimiter back to the default
delimiter ;

