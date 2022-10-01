BEGIN TRANSACTION ;

INSERT INTO dds.d_device_type (device_type, device_is_mobile)
SELECT DISTINCT (je.json_object::JSON->>'device_type') AS device_type,
		CASE WHEN (je.json_object::JSON->>'device_is_mobile') = 'true' THEN TRUE
		ELSE FALSE END AS device_is_mobile
FROM stg.json_events je
WHERE je.id > (SELECT CASE WHEN max(last_id::int) IS NULL THEN -1 ELSE  max(last_id::int) END AS last_id
		       FROM dds.d_service WHERE table_name = 'dds.d_device_type');

INSERT INTO dds.d_service (last_id, loaded_at, table_name)
SELECT max(id) AS last_id,
	   now() AS loaded_at ,
	   'dds.d_device_type' AS table_name
FROM stg.json_events  ;

COMMIT TRANSACTION ;