CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS bags(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_kind_counts JSONB DEFAULT '{}'
);

-- create type if it doesn't exist
DO $$ BEGIN
    IF to_regtype('item_kind') IS NULL THEN
        CREATE TYPE item_kind AS ENUM ('round', 'square', 'squiggly', 'other');
    ELSE
        raise notice 'item_kind type already exists, so not creating...';
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS items(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    kind item_kind,
    bag_id uuid REFERENCES bags (id)
);

CREATE OR REPLACE FUNCTION bag_items_count() RETURNS TRIGGER AS $$
    BEGIN
        /* IF (TG_OP = 'DELETE') THEN */
        /*     INSERT INTO emp_audit */
        /*         SELECT 'D', now(), user, o.* FROM old_table o; */
       -- Source of the trick https://stackoverflow.com/a/34680345/2252728
       -- TODO SELECT X INTO
       select json_object_agg(kind_counts.kind, kind_counts.item_count) into item_changes
       from (
        select kind, count(*) as item_count
        from items
        where group_id = 'e9a3f436-b03f-4ced-9e4a-1b0590c6c08b'
        group by kind
       ) as kind_counts;

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

DROP TRIGGER IF EXISTS bag_items_update ON items;
CREATE TRIGGER bag_items_update
    AFTER INSERT ON items
    REFERENCING NEW TABLE AS new_table
    FOR EACH STATEMENT EXECUTE FUNCTION bag_items_count();

-- TODO add UPDATE and DELETE
