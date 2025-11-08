import sqlite3


# Class-based context manager
class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        # Open the connection
        self.conn = sqlite3.connect(self.db_path)
        return self.conn  # This will be assigned to the 'as' variable

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection automatically
        if self.conn:
            self.conn.close()
        # Return False to propagate exceptions, True would suppress them
        return False


# Using the context manager
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

# Print the results
for row in results:
    print(row)
