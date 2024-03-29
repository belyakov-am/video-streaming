import aiohttp
import os

from tusclient import client

CLOUDFLARE_TOKEN = os.getenv('CLOUDFLARE_TOKEN')
CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')
CLOUDFLARE_DEBUG = os.getenv('CLOUDFLARE_DEBUG', None)
CLOUDFLARE_URL = 'https://api.cloudflare.com/client/v4/accounts/{}/stream'


def get_headers():
    return {'Authorization': f'Bearer {CLOUDFLARE_TOKEN}'}


def get_client() -> client.TusClient:
    return client.TusClient(
        CLOUDFLARE_URL.format(CLOUDFLARE_ACCOUNT_ID),
        headers=get_headers())


async def get_video_uid(url: str):
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.get(url) as r:
            json_body = await r.json()
            if json_body.get('result'):
                return json_body['result'].get('uid')


async def upload_file(file_stream):
    if CLOUDFLARE_DEBUG == '1':
        '''
        save video_id to file and send the file instead of video file
        echo 'video_id' > file_input
        /video/upload with file=file_input
        '''
        return str(file_stream.readline().strip().decode('utf-8'))

    new_client = get_client()

    uploader = new_client.async_uploader(
        file_stream=file_stream,
        chunk_size=5 * 1024 * 1024,
    )
    await uploader.upload()
    return await get_video_uid(uploader.url)
