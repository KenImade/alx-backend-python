# ¡/usr/bin/python3
import mysql.connector


def stream_users():
    """creates a generator that streams rows from an SQL database one by one"""
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host="localhost", user="user", password="password", database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
