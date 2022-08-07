CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS bags(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_kind_counts JSONB
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
    group_id integer REFERENCES bags (id)
);

