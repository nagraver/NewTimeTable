from connection.connections import col


async def append_data(data):
    data.clear()
    data.extend(col.find())
