import asyncio
from nats.aio.client import Client as NATS


# async def message_handler(msg):
#     print("message====================")
#     print(f"Received message: {msg}")


# async def consume_messages(subject, event):
#     nc = NATS()

#     try:
#         print("consumer========================")
#         await nc.connect(servers=["nats://nats:4222"])

#         # Use await when subscribing
#         await nc.subscribe('my_subject', cb=message_handler)

#         # Signal that the subscription is ready
#         event.set()
#     except Exception as e:
#         print(f"Error consuming messages: {e}")

#     finally:
#         await nc.close()
async def message_handler(msg):
    print("message====================")
    print(f"Received message: {msg}")

# async def consume_messages(subject, event):
#     nc = NATS()

#     try:
#         print("consumer========================")
#         await nc.connect(servers=["nats://nats:4222"])

#         # Use await when subscribing
#         await nc.subscribe(subject, cb=message_handler)

#         print("helloo=============")
#         # Signal that the subscription is ready
#         event.set()
#     except Exception as e:
#         print(f"Error consuming messages: {e}")
#     finally:
#         await nc.close()

async def consume_messages(subject, event):
   nc = NATS()

   try:
       print("consumer========================")
       await nc.connect(servers=["nats://nats:4222"])

       # Use await when subscribing
       await nc.subscribe(subject, cb=message_handler)

       print("Subscription established")
       # Signal that the subscription is ready
       event.set()
   except Exception as e:
       print(f"Error consuming messages: {e}")
   finally:
       await nc.close()