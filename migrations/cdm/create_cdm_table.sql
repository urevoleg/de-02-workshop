drop table if exists cdm.events_report;

create table if not exists cdm.events_report (
id serial primary key,
date_hour timestamp not null,
event_type varchar not null,
geo_name varchar not null,
referer_url varchar not null,
device_type varchar not null,
events_qty int not null default 0,
purchases_qty int not null default 0,
constraint cdm_events_report_events_qty_check check ((events_qty >= (0) :: numeric)),
constraint cdm_events_report_purchases_qty_check check ((purchases_qty >= (0) :: numeric))
);