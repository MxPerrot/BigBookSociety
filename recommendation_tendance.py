import psycopg2

connection = psycopg2.connect(database="pg_dgoupil", user="dgoupil", password="fqds;", host="servbdd", port=5432)

cursor = connection.cursor()