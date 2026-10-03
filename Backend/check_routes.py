from app.database.connection import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'routes'
    ORDER BY ordinal_position;
""")

columns = cursor.fetchall()

print("Routes table columns:")
for column in columns:
    print(column)

cursor.close()
connection.close()