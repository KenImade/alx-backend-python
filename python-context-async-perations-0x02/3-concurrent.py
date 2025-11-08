import asyncio
import aiosqlite


# Asynchronous function to fetch all users
async def async_fetch_users(db_path="users.db"):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


# Asynchronous function to fetch users older than 40
async def async_fetch_older_users(db_path="users.db"):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()


# Function to fetch both concurrently
async def fetch_concurrently():
    all_users_task = async_fetch_users()
    older_users_task = async_fetch_older_users()

    all_users, older_users = await asyncio.gather(all_users_task, older_users_task)

    print("All users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


# Run the concurrent fetch
asyncio.run(fetch_concurrently())
