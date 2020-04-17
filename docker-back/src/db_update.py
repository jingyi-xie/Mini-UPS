import os
import urllib.parse as up
import psycopg2

up.uses_netloc.append("postgres")
conn = psycopg2.connect(
    database="cobajydu",
    user="cobajydu",
    password="JKeoMazBOeXzE_dbVcBEUyUEZsIZz77s",
    host="rajje.db.elephantsql.com",
    port="5432"
)