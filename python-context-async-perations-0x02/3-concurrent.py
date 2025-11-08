import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    results = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    all_users, older_users = results
    print("All users:")
    for user in all_users:
        print(user)
    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
