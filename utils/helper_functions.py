import requests
from utils.const import UPLOAD_PHOTO_URL

async def upload_img_to_server(file):
    result = requests.post(UPLOAD_PHOTO_URL, files ={"image": file})
    print(result.json())
