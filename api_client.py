import aiohttp
import json

class APIClient:
    def __init__(self, url:str):
        self.url = url

    async def add_user(self, name:str, role:str, token_amount:int):
        body = {

            "name":name,
            "role":role,
            "token_amount":token_amount
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=f'{self.url}/users', json=body) as response:
                return await response.text()

    async def get_user(self, user_name:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.url}/users/{user_name}') as response:
                user = json.loads(await response.text())
                return user

    async def send_img_to_api(self, user_name, image_path, model):
        async with aiohttp.ClientSession() as session:
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()

                data = aiohttp.FormData()
                data.add_field('image', image_bytes, filename='image.jpg', content_type='image/jpeg')

                params = {'user_name': user_name}
                async with session.post(url=f'{self.url}/cv/{model}', data=data, params=params) as response:
                    if response.status == 202:
                        task_id = (await response.json())['task_id']
                        print(f'Task ID: {task_id}')
                        return task_id
                    else:
                        print(f'Error: {response.status} - {await response.text()}')
                        return 1


    async def get_img_to_api(self, task_id:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.url}/tasks/{task_id}') as response:
                if response.status == 200:
                    img = json.loads(await response.text())
                    return img
                elif response.status == 102:
                    return 0
                return 1

