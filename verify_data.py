import sqlite3

db_path = "/opt/fueltheaura-ai/data/supervisor_improvements.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check improvements table
print("📊 Improvements Table:")
cursor.execute("SELECT COUNT(*) FROM improvements")
print(f"   Total records: {cursor.fetchone()[0]}")

cursor.execute("SELECT category, COUNT(*) FROM improvements GROUP BY category")
print("   By category:")
for row in cursor.fetchall():
    print(f"      {row[0]}: {row[1]}")

cursor.execute("SELECT * FROM improvements ORDER BY timestamp DESC LIMIT 3")
print("\n   Sample records:")
for row in cursor.fetchall():
    print(f"      {row[1][:10]} | {row[2]} | {row[3]} | Impact: {row[7]}")

# Check SEO metrics table
print("\n📊 SEO Metrics Table:")
cursor.execute("SELECT COUNT(*) FROM seo_metrics")
print(f"   Total records: {cursor.fetchone()[0]}")

cursor.execute("SELECT * FROM seo_metrics ORDER BY timestamp DESC LIMIT 3")
print("   Sample records:")
for row in cursor.fetchall():
    print(f"      {row[1][:10]} | {row[2]} | Words: {row[9]} | Speed: {row[11]}")

# Check performance metrics table
print("\n📊 Performance Metrics Table:")
cursor.execute("SELECT COUNT(*) FROM performance_metrics")
print(f"   Total records: {cursor.fetchone()[0]}")

cursor.execute("SELECT metric_name, COUNT(*) FROM performance_metrics GROUP BY metric_name")
print("   By metric:")
for row in cursor.fetchall():
    print(f"      {row[0]}: {row[1]}")

conn.close()