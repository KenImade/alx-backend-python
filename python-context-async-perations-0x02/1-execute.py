import sqlite3


# Class-based context manager to execute a query
class ExecuteQuery:
    def __init__(self, db_path, query, params=None):
        self.db_path = db_path
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        # Execute the query with parameters
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  # Returned to the 'as' variable

    def __exit__(self, exc_type, exc_value, traceback):
        # Close connection automatically
        if self.conn:
            self.conn.close()
        # Return False to propagate exceptions
        return False


# Usage of the context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    for row in results:
        print(row)
