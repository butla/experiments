-- SQL to paste into the CLI and experiment with
CREATE OR REPLACE FUNCTION bag_items_count() RETURNS TRIGGER AS $$
    BEGIN
        /* IF (TG_OP = 'DELETE') THEN */
        /*     INSERT INTO emp_audit */
        /*         SELECT 'D', now(), user, o.* FROM old_table o; */
       -- Source of the trick https://stackoverflow.com/a/34680345/2252728

       -- TODO handle inserts into multiple bags
       -- TODO SELECT X INTO
       SELECT json_object_agg(kind_counts.kind, kind_counts.count_of_kind) INTO STRICT item_changes
       FROM (
        SELECT kind, count(*) AS count_of_kind
        FROM items
        WHERE group_id = 'e9a3f436-b03f-4ced-9e4a-1b0590c6c08b'
        GROUP BY kind
       ) AS kind_counts;

       -- version with more intermittent vars
       select kind, count(*) as item_count into kind_counts_rows
       from items
       where group_id = 'e9a3f436-b03f-4ced-9e4a-1b0590c6c08b'
       group by kind;

       select jsonb_object_agg(kind, item_count) into kind_counts_json
       from kind_counts_rows;

       -- TODO update bag with kind_counts_json

        /* IF (TG_OP = 'UPDATE') THEN */
        /*     -- implement for multiple bags in the update */
        /*     -- TODO select bag for update first */
        /*     UPDATE bags SET */
        /*     INSERT INTO emp_audit */
        /*         SELECT 'U', now(), user, 'whatever', sum(n.salary) FROM new_table n; */
        /* ELSIF (TG_OP = 'INSERT') THEN */
        /*     INSERT INTO emp_audit */
        /*         SELECT 'I', now(), user, 'whatever', sum(n.salary) FROM new_table n; */
        /* END IF; */
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$$ LANGUAGE plpgsql;
