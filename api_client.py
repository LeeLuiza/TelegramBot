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
                if response.status == 200:
                    user = json.loads(await response.text())
                    return user
                else:
                    return True

    async def get_all_user(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.url}/users/') as response:
                if response.status == 200:
                    users = json.loads(await response.text())
                    return users
                else:
                    return True

    async def check_user(self, user_name:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.url}/users/{user_name}') as response:
                if response.status == 200:
                    return False
                else:
                    return True

    async def use_yolo8(self, user_name, image_path, model):
        async with aiohttp.ClientSession() as session:
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()

                data = aiohttp.FormData()
                data.add_field('image', image_bytes, filename='image.jpg', content_type='image/jpeg')

                params = {'user_name': user_name}
                async with session.post(url=f'{self.url}/cv/models/{model}', data=data, params=params) as response:
                    if response.status == 202:
                        task_id = (await response.json())['task_id']
                        print(f'Task ID: {task_id}')
                        return task_id
                    else:
                        print(f'Error: {response.status} - {await response.text()}')
                        return 1

    async def get_result(self, task_id:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.url}/cv/models/tasks/{task_id}') as response:
                if response.status == 200:
                    task_result = await response.json()
                    return task_result
                elif response.status == 202:
                    return 0
                return 1

    async def get_history(self, user_name:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.url}/cv/models/tasks/history/{user_name}') as response:
                if response.status == 200:
                    history = json.loads(await response.text())
                    return history
                else:
                    return True

    async def get_cost_model(self, model:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.url}/cv/models/{model}') as response:
                if response.status == 200:
                    cost_model = json.loads(await response.text())
                    return cost_model
                else:
                    return True

    async def change_token(self, user_name:str, token_amount:int):

        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f'{self.url}/users/{user_name}/tokens', params=[('token_amount', token_amount)]) as response:
                return await response.text()

    async def change_role(self, user_name:str, new_role:str):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f'{self.url}/users/{user_name}/role', params=[('new_role', new_role)]) as response:
                return await response.text()

    async def change_model_cost(self, model_name:str, new_cost:int):

        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f'{self.url}/cv/models/{model_name}/cost', params=[('new_cost', new_cost)]) as response:
                return await response.text()
