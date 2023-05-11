# Fitzlab Data Manager

An extremely simple application for storing experimental
data in a database.  The data is stored in a single table, 
unless otherwise specified

We use SQLite for this application due to its
immense simplicity and because there is no need
to cross-reference between multiple experiments,
at least right now

## Installation

1. Clone the repository
2. Install the requirements
3. Import as a module (import data_manager as dm)

## Usage

### Creating a new database

Note well, when creating a database, only one table will be created by default. 
The name of this table, if left blank in the arguments for `setup_experiment` will 
default to the name of the database, minus the extension.

```python
import data_manager as dm

# Create a new experiment - first define the schema for the table AS A DICTIONARY
# @see https://www.sqlite.org/datatype3.html
# Only a few types are supported right now
db = "my_database.db"
schema = {"column1": "INTEGER", "column2": "TEXT", "column3": "REAL"}
dm.setup_experiment(schema, db)

# Insert data into the table

# Example for data. NOTE THAT THE KEYS MUST MATCH THE SCHEMA
# AND THE DATATYPES MUST MATCH THE SCHEMA
data = {
    "id": [1, 2, 3],
    "name": ["Alex", "Bob", "Charlie"],
    "age": [20, 30, 40]
}
dm.insert_from_dict(data, db)
```

### Querying the database

No wrapper support for querying the database. Use Raw sql to select data

```python
import data_manager as dm
import sqlite3

db = "my_database.db"
sql = "SELECT * FROM my_table"
conn = sqlite3.connect("test.db")
cur = conn.cursor()

cur.execute("""SELECT * FROM test WHERE name = "Alex";""")
print(cur.fetchall())

conn.close()
```