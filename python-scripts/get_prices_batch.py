import datetime
import time
import aiohttp
import asyncio
import json
import random
import argparse

# start timer

start_time = time.time()

parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-p", "--products", help = "amount of products")
parser.add_argument("-b", "--batch", help = "amount of products per batch")

args = parser.parse_args()

PRODUCTS_AMOUNT = int(args.products) if args.products else 100
BATCH = int(args.batch) if args.batch else 10

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
data = [generate_items(id=i) for i in range(1, PRODUCTS_AMOUNT)]

# split into chunks of 10
chunks = [data[i:i + 10] for i in range(0, len(data), BATCH)]

print(f'About to send {len(data)} items in {len(chunks)} chunks of {BATCH} items')

# Define a coroutine that sends a POST request
async def post(session, url, data):
    async with session.post(url, data=json.dumps(data)) as response:
        return await response.text()

# Define a coroutine that creates a session and sends all requests
async def main():
    chunks_list = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for chunk in chunks:
            # task = asyncio.ensure_future(post(session, 'https://next-pricing-edge-test.vercel.app/api/pricing/', chunk))
            task = asyncio.ensure_future(post(session, 'http://localhost:3000/api/pricing-batch/', {
                "products": chunk
            }))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        # handle the responses here
        for response in responses:
            # print(response)
            # parse the response as JSON
            response = json.loads(response)
            chunks_list.append(response)
    
    print(f'Got {len(chunks_list)} chunks')

    # merge chunks
    prices = [item for sublist in chunks_list for item in sublist]

    print(f'Got {len(prices)} prices')
    
    # sort them by biggest price
    prices.sort(key=lambda x: x['totalPrice'], reverse=True)
    

    # print the top 10
    # print(prices[:10])
    # print(prices)

# Run the script
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# end timer
end_time = time.time()

print(f"Execution time: {end_time - start_time} seconds")