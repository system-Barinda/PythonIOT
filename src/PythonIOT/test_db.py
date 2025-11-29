import asyncio
from src.core.database import Database   # correct for module execution


async def main():
    db = Database()
    await db.connect()
    print("Connected successfully!")
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
