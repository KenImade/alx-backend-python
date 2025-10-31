#!/usr/bin/python3
import mysql.connector

seed = __import__("seed")


def stream_users_in_batches(batch_size):
    """Fetches rows in batches"""
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()

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


def batch_processing(batch_size):
    """Processes data in batches"""
    for user in stream_users_in_batches(batch_size):
        if int(user["age"]) > 25:
            print(user)
