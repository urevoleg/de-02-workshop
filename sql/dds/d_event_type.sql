BEGIN TRANSACTION ;

INSERT INTO dds.d_event_type (event_type_name)
SELECT DISTINCT
		CASE WHEN (je.json_object::JSON->>'page_url_path') LIKE '%product%' THEN 'product'
		ELSE substring((je.json_object::JSON->>'page_url_path'), 2) END AS event_type_name
FROM stg.json_events je
WHERE je.id > (SELECT CASE WHEN max(last_id::int) IS NULL THEN -1 ELSE  max(last_id::int) END AS last_id
		       FROM dds.d_service WHERE table_name = 'dds.d_event_type');;

INSERT INTO dds.d_service (last_id, loaded_at, table_name)
SELECT max(id) AS last_id,
	   now() AS loaded_at ,
	   'dds.d_event_type' AS table_name
FROM stg.json_events  ;

COMMIT TRANSACTION ;