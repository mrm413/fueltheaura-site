import sqlite3
import json

# Connect to the database
db_path = "/opt/fueltheaura-ai/data/ml_predictions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Database Tables:")
for table in tables:
    print(f"- {table[0]}")

# Get schema for each table
print("\nTable Schemas:")
for table in tables:
    print(f"\n{table[0]}:")
    cursor.execute(f"PRAGMA table_info({table[0]});")
    columns = cursor.fetchall()
    for column in columns:
        print(f"  {column[1]} ({column[2]})")

# Check contents of each table
print("\nTable Contents:")

for table in tables:
    print(f"\n{table[0]}:")
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
    count = cursor.fetchone()[0]
    print(f"  Row count: {count}")
    
    if count > 0:
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"  {row}")
    else:
        print("  Table is empty")

conn.close()