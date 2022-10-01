DROP TABLE IF EXISTS stg.json_events;
CREATE TABLE stg.json_events  (
	id serial PRIMARY KEY,
	event_id VARCHAR NOT NULL,
	event_timestamp timestamp,
	json_object text
);

CREATE INDEX idx_json_events_event_timestamp ON stg.json_events USING btree (event_timestamp);