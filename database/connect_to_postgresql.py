import psycopg2

try:
    # Establish a connection to the database
    conn = psycopg2.connect(
        database="robintest",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"  # Default PostgreSQL port
    )
    print("Connected succesfully to database")

    cursor = conn.cursor()
    sql_query = "select * from test"
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()

except Exception as e:
    print(f"An error occurred: {e}")
