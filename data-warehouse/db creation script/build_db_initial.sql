create database ecommerce_initial;

use ecommerce_initial;

create table vendors (
	vendor_id int not null,
    name varchar(200) not null,
    phone_number varchar(20) not null,
    address varchar(200) not null,
    zipcode mediumint not null,
    city varchar(50) not null,
    commission_rate decimal(2,2) not null,
    primary key (vendor_id)
);

create table products (
	product_id int not null,
    name varchar(100) not null,
    details varchar(1000),
    category varchar(20) not null,
    image_url varchar(500),
    vendor_id int not null,
    price decimal(9,2) not null,
    primary key (product_id),
    foreign key (vendor_id) references vendors(vendor_id)
);

create table customers (
	customer_id int not null,
    full_name varchar(200) not null,
    phone_number varchar(20) not null,
    address varchar(200) not null,
    zipcode mediumint not null,
    city varchar(50) not null,
    is_member bool not null default False,
    email varchar(200),
    primary key (customer_id)
);

create table orders (
	order_id bigint not null,
    customer_id int not null,
    product_id int not null,
	quantity smallint not null,
    price decimal(9,2) not null,
    total_cost decimal(10,2) not null,
    order_status varchar(200),
    order_costs decimal(9,2) not null,
    primary key (order_id),
    foreign key (customer_id) references customers(customer_id),
    foreign key (product_id) references products(product_id)
);

create table reviews (
	review_id bigint not null,
    customer_id int not null,
    product_id int not null,
	description varchar(1000),
    rating tinyint not null,
    primary key (review_id),
    foreign key (customer_id) references customers(customer_id),
    foreign key (product_id) references products(product_id)
);

create table sessions (
	session_id bigint not null,
    customer_id int not null,
    start_at timestamp not null default current_timestamp,
    end_at timestamp,
    primary key (session_id),
    foreign key (customer_id) references customers(customer_id)
);




