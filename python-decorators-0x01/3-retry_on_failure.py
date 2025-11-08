import time
import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(db_path, *args, **kwargs):
        conn = sqlite3.connect(db_path)
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result

    return wrapper


def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    if attempts == retries:
                        raise  # Re-raise the last exception
                    time.sleep(delay)

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
