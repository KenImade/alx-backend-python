import sqlite3
import functools

#### decorator to lof SQL queries


def log_queries(func):
    """Logs queries from database"""

    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"Query executed: {query}")
        return func(query, *args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
