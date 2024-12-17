"""Command handler script"""
import sys
import asyncio

from scripts.commands.migrate import migrate
from scripts.commands.seed import seed


async def command_handler():
    command = sys.argv[1]
    if command == "migrate":
        await migrate()
        if '--seed' in sys.argv:
            await seed()

    elif command == "seed":
        await seed()
        
    return


asyncio.run(command_handler())
