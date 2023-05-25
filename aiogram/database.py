import mysql.connector
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
)

async def signIn(username: str, password: str) -> bool:
    try:
        mycursor = mydb.cursor()
        mycursor.execute('SELECT password FROM users WHERE username = SHA1(%s)', (username,))
        myresult = mycursor.fetchone()
        if (len(myresult) == 0): return False
        dbPassword = myresult[0].decode()
        inputPassword = hashlib.sha1(password.encode("utf-8")).hexdigest()
        if (dbPassword == inputPassword): return True

        return False

    except mysql.connector.Error as error:
        print(f'An error occured: {error}')
        return False

async def signUp(username: str, password: str) -> bool: 
    try:
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO users (username, password) VALUES (SHA1(%s), SHA1(%s))', (username, password))
        return True

    except mysql.connector.Error as error:
        print(f'An error occured: {error}')
        return False