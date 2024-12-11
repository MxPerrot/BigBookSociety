import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2

# loading variables from .env file
load_dotenv() 

connection = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"), 
    user=os.getenv("USERNAME"), 
    password=os.getenv("PASSWORD"), 
    host=os.getenv("HOST"), 
    port=os.getenv("PORT")
)

cursor = connection.cursor()