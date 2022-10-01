/*
 * STG
 * Структура `events_service`:
- `id`
- `filename` - имя загруженного файла
- `uploaded_at` - время загрузки в `stg` слой
- `row_count` - кол-во загруженных строк
 */
-- migrations
CREATE TABLE stg.events_service (
	id serial PRIMARY KEY,
	filename VARCHAR(100) UNIQUE NOT NULL,
	uploaded_at timestamp NOT NULL,
	row_count int NOT NULL
);

CREATE UNIQUE INDEX events_service_filename_idx ON stg.events_service USING btree (filename);



