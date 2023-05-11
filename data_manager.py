"""
Data manager for experiments

@author Alex Carney
"""

import sqlite3


def setup_experiment(data_model: dict, db_file_name: str, db_table_name: str = ""):
    """
    Starts a new database representing the output of an experiment
    :param db_table_name: Name of the table to store the experiment results in, defaults to db_file_name
    :param data_model: A dictionary representing the schema for the experiment, see documentation for more information
    :param db_file_name: The name of the database file to be created. Use ":memory:" for test db
    :return:
    """
    # If no table name is specified, use the database name
    # but strip the .db at the end of the file name
    if db_table_name == "":
        db_table_name = db_file_name.replace(".db", "")

    conn = sqlite3.connect(db_file_name)
    cur = conn.cursor()

    # Generate the columns string for the CREATE TABLE statement
    columns_str = ', '.join([f"{column} {datatype}" for column, datatype in data_model.items()])

    # Create the table
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {db_table_name} ({columns_str});"
    cur.execute(create_table_sql)

    conn.commit()
    conn.close()


def insert_from_dict(result_dict: dict, db_file_name: str, db_table_name: str = ""):
    """
    Insert the results stored in a dictionary into the database.
    Note that the keys of the database should match with the data model that created the database

    WARNING: Must be run AFTER database is created, will not create a database automatically if it does not exist

    :param result_dict: A dictionary representing the results of an experiment
    :param db_file_name: Name of experiment database to insert into
    :param db_table_name: Name of table to insert into, defaults to db_file_name
    :return:
    """

    if db_table_name == "":
        db_table_name = db_file_name.replace(".db", "")

    columns = list(result_dict.keys())
    row_count = len(next(iter(result_dict.values())))

    # Convert the data_dict into a list of tuples representing rows
    data_rows = [tuple(result_dict[col][i] for col in columns) for i in range(row_count)]

    # Prepare the SQL insert statement
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?' for _ in columns])
    insert_sql = f"INSERT INTO {db_table_name} ({columns_str}) VALUES ({placeholders})"

    conn = sqlite3.connect(db_file_name)
    cur = conn.cursor()

    # Create the table if it does not exist
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {db_table_name} ({columns_str});"
    cur.execute(create_table_sql)

    # Perform the bulk insert
    cur.executemany(insert_sql, data_rows)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
