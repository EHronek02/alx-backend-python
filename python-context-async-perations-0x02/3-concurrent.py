#!/usr/bin/env python3
"""runs multiple data query concurrently using asyncio.gather"""
import asyncio
import aiosqlite


async def async_fetch_users():
    """fetch all users from the db"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            print("Fetching all users")
            users = await cursor.fetchall()
            print(f"Found {len(users)} users")
            return users


async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            print("Fetching older users...")
            users = await cursor.fetchall()
            print(f"Found {len(users)} users over 40")
            return users


async def fetch_concurrently():
    """Run all queries concurrently"""
    print("Starting concurrently queries...")
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    all_users, old_users = results

    print("\n Results:")
    print(f"Total users: {len(all_users)}")
    print(f"Users over 40: {len(old_users)}")

    return results


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
