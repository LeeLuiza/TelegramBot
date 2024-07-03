from api_client import APIClient
import asyncio

async def main():
    client = APIClient('http://127.0.0.1:8000')

    await client.add_user('name','client', 10)
    # print(await client.get_user('name'))

    print(await client.add_img_yolo8m('name', ))

if __name__=="__main__":
    asyncio.run(main())
