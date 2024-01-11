import asyncio
from nats.aio.client import Client as NATS


async def message_handler(msg):
    print(f"Received message: {msg}")

async def subscribe(subject):
    loop = asyncio.get_event_loop()  # Get the current event loop
    asyncio.set_event_loop(loop)  # Set the event loop

    nc = NATS()
    print("inside nc")

    await nc.connect(servers=["nats://nats:4222"])
    await nc.subscribe(subject, cb=message_handler)

    try:
        await nc.wait_closed()
    finally:
        await nc.close()