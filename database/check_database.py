

import sqlite3

conn = sqlite3.connect("database/tennis_analytics.db")

cursor = conn.cursor()

# Show all tables
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

tables = cursor.fetchall()

print("\nTables in Database\n")

for table in tables:

    table_name = table[0]

    print(f"\n===== {table_name} =====")

    cursor.execute(f"PRAGMA table_info({table_name});")

    columns = cursor.fetchall()

    for column in columns:
        print(column)

conn.close()


