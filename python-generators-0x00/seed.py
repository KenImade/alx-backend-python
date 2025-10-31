#!/usr/bin/python3
import uuid
import mysql.connector
import csv


def connect_db():
    """Connects to the MySQL Database server"""
    try:
        connection = mysql.connector.connect(
            host="localhost", user="username", password="password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev"""
    try:
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()


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


def create_table(connection):
    """Creates a table user_data"""
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id (Primary Key, UUID),
        name (VARCHAR, NOT NULL),
        email (VARCHAR, NOT NULL),
        age (DECIMAL, NOT NULL)),
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_table(connection, data):
    """Inserts data in the database if it does not exist"""
    cursor = connection.cursor()
    try:
        with open(data, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = int(row["age"])

                query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """

                cursor.execute(query, (user_id, name, email, age))

        connection.commit()
    except FileNotFoundError:
        print(f"Error: File '{data}' not found.")
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        cursor.close()
