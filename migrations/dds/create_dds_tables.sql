--create schema if not exists dds;

drop table if exists dds.service cascade;
drop table if exists dds.d_browser_name cascade;
drop table if exists dds.d_device_type cascade;
drop table if exists dds.d_geo cascade;
drop table if exists dds.d_os cascade;
drop table if exists dds.d_event_type cascade;
drop table if exists dds.d_referer_url cascade;
drop table if exists dds.d_user_custom_id cascade;
drop table if exists dds.d_utm_source cascade;
drop table if exists dds.d_utm_campaign cascade;
drop table if exists dds.d_event_timestamp cascade;
drop table if exists dds.f_events cascade;


create table if not exists dds.d_service (
id serial primary key,
last_id varchar,
table_name varchar,
loaded_at timestamp
);

create table if not exists dds.d_browser_name (
browser_id serial primary key,
browser_name varchar unique not null);

create table if not exists dds.d_device_type(
device_id serial primary key,
device_type varchar unique not null,
device_is_mobile bool);

create table if not exists dds.d_geo (
geo_id serial primary key,
geo_country varchar not null,
/*не могу поставить unique потому что могут быть
  несколько таймзон*/
geo_region_name varchar not null, 
geo_timezone varchar not null
);

CREATE TABLE IF NOT EXISTS dds.d_os(
os_id serial PRIMARY KEY,
os_name varchar UNIQUE not null);

CREATE TABLE IF NOT EXISTS dds.d_event_type (
event_type_id serial PRIMARY KEY,
event_type_name varchar UNIQUE not null);

CREATE TABLE IF NOT EXISTS dds.d_referer_url (
referer_id serial PRIMARY KEY,
referer_medium varchar,
referer_url varchar UNIQUE not null
);

CREATE TABLE IF NOT EXISTS dds.d_user_custom_id (
user_id serial PRIMARY KEY,
user_custom_id varchar UNIQUE not null
--user_domain_id varchar --не добавляю, не уникальный
);

--пока без источника, но с кампанией, где указан источник
--create table if not exists dds.d_utm_source (
--source_id serial primary key,
--utm_source_name varchar unique);
CREATE TABLE IF NOT EXISTS dds.d_utm_campaign (
utm_campaign_id serial PRIMARY KEY,
utm_campaign_name varchar not null,
utm_source varchar not null,
utm_content varchar not null,
UNIQUE (utm_campaign_name,
utm_source,
utm_content)
);

CREATE TABLE IF NOT EXISTS dds.d_event_timestamp (
	event_timestamp_id serial PRIMARY KEY,
	ts timestamp NOT NULL,
	"year" int2 NOT NULL,
	"month" int2 NOT NULL,
	"day" int2 NOT NULL,
	"time" time NOT NULL,
	"date" date NOT NULL,
	CONSTRAINT dm_delivery_timestamps_day_check CHECK (
		(
			(DAY >= 1)
AND (DAY <= 31)
		)
	),
	CONSTRAINT dm_delivery_timestamps_month_check CHECK (
		(
			(MONTH >= 1)
AND (MONTH <= 12)
		)
	),
	CONSTRAINT dm_delivery_timestamps_year_check CHECK (
		(
			(YEAR >= 2022)
AND (YEAR < 2500)
		)
	)
);




create table if not exists dds.f_events (
id serial primary key,
user_id int,
event_type_id int,
event_timestamp_id int,
geo_id int,
os_id int,
referer_id int,
utm_campaign_id int,
device_id int,
constraint f_events_user_id_fkey foreign key (user_id) references dds.d_user_custom_id(user_id),
constraint f_events_event_type_id_fkey foreign key (event_type_id) references dds.d_event_type(event_type_id),
constraint f_events_event_timestamp_id_fkey foreign key (event_timestamp_id) references dds.d_event_timestamp(event_timestamp_id),
constraint f_events_geo_id_fkey foreign key (geo_id) references dds.d_geo(geo_id),
constraint f_events_os_id_fkey foreign key (os_id) references dds.d_os(os_id),
constraint f_events_referer_id_fkey foreign key (referer_id) references dds.d_referer_url(referer_id),
constraint f_events_utm_campaign_id_fkey foreign key (utm_campaign_id) references dds.d_utm_campaign(utm_campaign_id),
constraint f_events_device_id_fkey foreign key (device_id) references dds.d_device_type(device_id)
);