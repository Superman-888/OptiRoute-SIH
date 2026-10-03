from app.database.connection import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT *
    FROM routes
    LIMIT 5;
""")

rows = cursor.fetchall()

print("Existing route records:")
for row in rows:
    print(row)

cursor.close()
connection.close()