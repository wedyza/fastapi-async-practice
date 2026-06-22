import asyncio
import sys

from arq.cli import cli

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    sys.exit(cli.main())
finally:
    loop.close()
