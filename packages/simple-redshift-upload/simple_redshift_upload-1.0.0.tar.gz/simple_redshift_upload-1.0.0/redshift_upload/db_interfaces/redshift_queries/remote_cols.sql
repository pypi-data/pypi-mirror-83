SELECT a.attname
FROM pg_class c, pg_attribute a, pg_type t
WHERE c.relname = %(table_name)s
   AND a.attnum > 0
   AND a.attrelid = c.oid
   AND a.atttypid = t.oid
order by attnum
