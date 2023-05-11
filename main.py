import data_manager as dm
import sqlite3

# Create example table
data_model = {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT",
    "age": "INTEGER"
}

dm.setup_experiment(data_model, "test.db", "test_table")

# Insert some data
data = {
    "id": [1, 2, 3],
    "name": ["Alex", "Bob", "Charlie"],
    "age": [20, 30, 40]
}

dm.insert_from_dict(data, "test.db", "test_table")

# Read the data back
conn = sqlite3.connect("test.db")
cur = conn.cursor()

cur.execute("""SELECT * FROM test_table WHERE name = "Alex";""")
print(cur.fetchall())

conn.close()
