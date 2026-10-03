from app.database.connection import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(table[0])

cursor.close()
connection.close()