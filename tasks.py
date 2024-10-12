import asyncio

from api.tasks import start_app_tasks

asyncio.run(start_app_tasks())
# loop.run_until_complete(start_app_tasks())
