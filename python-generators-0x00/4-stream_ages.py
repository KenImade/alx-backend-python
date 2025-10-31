#!/usr/bin/python3
import mysql.connector

seed = __import__("seed")


def stream_user_ages():
    """
    Generator to compute a memory-efficient aggregrate function.
    i.e average age for a large dataset
    """

    connection = None
    cursor = None

    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            yield row["age"]

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def calculate_average_age():
    """Calculates average age"""

    total_age = 0
    count = 0

    for age in stream_user_ages():
        if age is not None:
            total_age += int(age)
            count += 1

    if count == 0:
        print("No users found.")

    avg_age = total_age / count

    print(f"Average age of users: {avg_age:.2f}")
