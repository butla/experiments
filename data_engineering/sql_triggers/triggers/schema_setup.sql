CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===== TYPE DEFINITIONS =====
-- create type if it doesn't exist
DO $$ BEGIN
    IF to_regtype('item_kind') IS NULL THEN
        CREATE TYPE item_kind AS ENUM ('round', 'square', 'squiggly', 'other');
    ELSE
        raise notice 'item_kind type already exists, so not creating...';
    END IF;
END $$;

-- ===== TABLE DEFINITIONS =====
CREATE TABLE IF NOT EXISTS bags(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_kind_counts JSONB DEFAULT '{}'
);


CREATE TABLE IF NOT EXISTS items(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    kind item_kind,
    bag_id uuid REFERENCES bags (id)
);

-- ===== FUNCTION DEFINITIONS =====
-- Related doc links:
-- https://www.postgresql.org/docs/current/plpgsql-declarations.html
-- https://www.postgresql.org/docs/current/plpgsql-statements.html#PLPGSQL-STATEMENTS-ASSIGNMENT
-- https://www.postgresql.org/docs/current/functions-aggregate.html


CREATE OR REPLACE FUNCTION bag_items_count(bag_id_to_count uuid) RETURNS jsonb AS $$
DECLARE
    -- I wanted to have variables for the sub-select results, but apparently, they don't exist.
    -- https://stackoverflow.com/questions/24949266/select-multiple-rows-and-columns-into-a-record-variable
    item_changes jsonb;
BEGIN
    WITH kind_counts AS (
       SELECT kind, count(*) AS count_of_kind
       FROM items
       WHERE bag_id = bag_id_to_count
       GROUP BY kind
    )
    SELECT json_object_agg(kind_counts.kind, kind_counts.count_of_kind) INTO STRICT item_changes
    FROM kind_counts;

    RETURN item_changes;
END;
$$ LANGUAGE plpgsql;

/* CREATE OR REPLACE FUNCTION bag_items_count() RETURNS TRIGGER AS $$ */
/*     BEGIN */
/*         /1* IF (TG_OP = 'DELETE') THEN *1/ */
/*         /1*     INSERT INTO emp_audit *1/ */
/*         /1*         SELECT 'D', now(), user, o.* FROM old_table o; *1/ */
/*        -- Source of the trick https://stackoverflow.com/a/34680345/2252728 */

/*        -- TODO handle inserts into multiple bags */
/*        -- TODO SELECT X INTO */
/*        SELECT json_object_agg(kind_counts.kind, kind_counts.count_of_kind) INTO STRICT item_changes */
/*        FROM ( */
/*         SELECT kind, count(*) AS count_of_kind */
/*         FROM items */
/*         WHERE group_id = 'e9a3f436-b03f-4ced-9e4a-1b0590c6c08b' */
/*         GROUP BY kind */
/*        ) AS kind_counts; */

/*        -- version with more intermittent vars */
/*        select kind, count(*) as item_count into kind_counts_rows */
/*        from items */
/*        where group_id = 'e9a3f436-b03f-4ced-9e4a-1b0590c6c08b' */
/*        group by kind; */

/*        select jsonb_object_agg(kind, item_count) into kind_counts_json */
/*        from kind_counts_rows; */

/*        -- TODO update bag with kind_counts_json */

/*         /1* IF (TG_OP = 'UPDATE') THEN *1/ */
/*         /1*     -- implement for multiple bags in the update *1/ */
/*         /1*     -- TODO select bag for update first *1/ */
/*         /1*     UPDATE bags SET *1/ */
/*         /1*     INSERT INTO emp_audit *1/ */
/*         /1*         SELECT 'U', now(), user, 'whatever', sum(n.salary) FROM new_table n; *1/ */
/*         /1* ELSIF (TG_OP = 'INSERT') THEN *1/ */
/*         /1*     INSERT INTO emp_audit *1/ */
/*         /1*         SELECT 'I', now(), user, 'whatever', sum(n.salary) FROM new_table n; *1/ */
/*         /1* END IF; *1/ */
/*         RETURN NULL; -- result is ignored since this is an AFTER trigger */
/*     END; */
/* $$ LANGUAGE plpgsql; */

/* DROP TRIGGER IF EXISTS bag_items_update ON items; */
/* CREATE TRIGGER bag_items_update */
/*     AFTER INSERT ON items */
/*     REFERENCING NEW TABLE AS new_table */
/*     FOR EACH STATEMENT EXECUTE FUNCTION bag_items_count(); */

-- TODO add UPDATE and DELETE
