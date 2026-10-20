import sqlite3

# Connect to your database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all rows from the urls table
cursor.execute("SELECT * FROM urls")
rows = cursor.fetchall()

print("\n--- DATABASE CONTENTS ---")
for row in rows:
  print(f"ID: {row[0]} | Long URL: {row[1]}")

conn.close()