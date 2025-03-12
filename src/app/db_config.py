import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo:mongo@mongodb:27017/")
db = client.analytics
