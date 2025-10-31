#!/usr/bin/python3
import mysql.connector


def connect_to_prodev():
    """Connects the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password",
            database="ALX_prodev",
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        return None


def stream_users_in_batches(batch_size):
    """Fetches rows in batches"""
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()

        if not connection:
            return

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            for row in batch:
                yield row

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processsing(batch_size):
    """Processes data in batches"""
    for user in stream_users_in_batches(batch_size):
        if int(user["age"]) > 25:
            print(user)
