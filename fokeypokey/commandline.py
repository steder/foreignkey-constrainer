from pprint import pprint

from .db import metadata


def are_you_probably_foreign_key(column) -> bool:
    if not column.primary_key:
        norm_name = column.name.lower()
        if norm_name.endswith("id"):
            return True
    return False


def main():
    table_names = []
    # names of columns that maybe should be foreign keys:
    possible_foreign_keys = []
    current_foreign_keys = []

    for name, table in sorted(metadata.tables.items()):
        table_names.append(name.lower())
        print("table: ", name)
        #import pdb; pdb.set_trace()
        for column in table.columns:
            print("column: ", column)
            if column.foreign_keys:
                # if it already has foreign keys, great!
                for key in column.foreign_keys:
                    print("FK: ", key)
                    current_foreign_keys.append((name, column, key))

            elif are_you_probably_foreign_key(column):
                possible_foreign_keys.append(column)

            print("Possible foreign keys on table: {}".format(name))



    automatic_keys = []
    manual_keys = []
    missing_primary_keys = []

    for column in possible_foreign_keys:
        table_name = column.name.lower()[0:-2]
        if table_name in table_names:
            if table_name == column.table.name:
                missing_primary_keys.append(column)
            else:
                print("PFK: {} from {} to {}".format(column, column.table, table_name))
                automatic_keys.append((column, column.table, table_name))
        else:
            print("PFK: {}, not sure what this links to".format(column))
            manual_keys.append(column)

    print("Foreign Keys we have to handle manually ({}):".format(len(manual_keys)))
    for key in manual_keys:
        print(key.table.name + "." + key.name)

    # Add the constraint initially with "NOT VALID"...
    auto_foreign_key_sql = """
    ALTER TABLE {table} ADD {constraint_name} FOREIGN_KEY ({column_name}) REFERENCES {target_table} NOT VALID;
    """.strip()
    # Then make the constraint valid by doing any necessary
    # data cleanup and running:


    print("Foreign Keys we can create automatically ({}):".format(len(automatic_keys)))
    with open("fokeys.sql", "w") as sqlfile:
        sqlfile.write("BEGIN;\n")
        for column, src, target in automatic_keys:
            print(src.name + "." + column.name + " -> " + target)
            sql = auto_foreign_key_sql.format(**{
                "table": column.table.name,
                "constraint_name": "{}_to_{}_fk".format(column.table.name, target),
                "column_name": column.name,
                "target_table": target,
            })
            sqlfile.write(sql + '\n')
        sqlfile.write("ROLLBACK;\n")
    print("Generated SQL: fokeys.sql")

    print("Missing Primary Keys ({}):".format(len(missing_primary_keys)))
    for column in missing_primary_keys:
        print(column)

    print("Current foreign keys ({}):".format(len(current_foreign_keys)))
    for key in current_foreign_keys:
        print(key)
