import datetime
import aiohttp
import asyncio
import json
import random

def add_days(date: str, days: int):
    return (datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=days)).strftime('%Y-%m-%d')

def get_random_price():
    return random.randint(10, 200)

def get_random_date_in_future():
    return add_days('2022-01-01', random.randint(0, 365))

def generate_items(id: int):
    return {
        "id": id,
        "startDate": "2022-01-01",
        "endDate": get_random_date_in_future(),
        "basePrice": get_random_price(),
        "rules": [
            {
                "minStayLength": random.randint(1, 30),
                "priceModifier": -random.randint(10, 50)
            },
            {
                "date": "2022-01-04",
                "fixedPrice": 20
            }
        ]
    }

# Define your data
data = [generate_items(id=i) for i in range(1, 100)]

print(f'About to send {len(data)} items')

# Define a coroutine that sends a POST request
async def post(session, url, data):
    async with session.post(url, data=json.dumps(data)) as response:
        return await response.text()

# Define a coroutine that creates a session and sends all requests
async def main():
    prices = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in data:
            task = asyncio.ensure_future(post(session, 'http://localhost:3000/api/pricing/', item))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        # handle the responses here
        for response in responses:
            # print(response)
            # parse the response as JSON
            response = json.loads(response)
            prices.append(response)
    
    print(f'Got {len(prices)} prices')

    # sort them by biggest price
    prices.sort(key=lambda x: x['totalPrice'], reverse=True)
    # print the top 10
    print(prices[:10])
    # print(prices)

# Run the script
loop = asyncio.get_event_loop()
loop.run_until_complete(main())