import asyncio
import base64
import json

import aiohttp
import cv2
import numpy as np
from celery import Celery

celery_app = Celery(
    "tasks", backend="redis://redis", broker="pyamqp://guest:guest@rabbitmq//"
)

MLSERVER_URL: str = "http://ml:8080/v2/models/yolov10-model/infer"


async def async_post_request_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()


async def async_post_request(url, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json) as response:
            return await response.json()


async def decompose(image, lw, lh):
    height, width = image.shape[:2]  # Extracting height and width
    url = f"http://noise-reduction:8085/decompose?width={width}&height={height}&lw={lw}&lh={lh}"
    image_data = image.flatten().tolist()
    json_payload = json.dumps(image_data)
    payload = await async_post_request_data(url, json_payload)
    if "error" in payload or len(payload) < height or len(payload[0]) < width:
        return image

    for i in range(height):
        for j in range(width):
            value = payload[i][j]
            if value > 255:
                value = 255
            if value < 0:
                value = 0
            image[i, j] = value
    return image


def pimage(payload, image_size):
    image = cv2.imdecode(payload, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    max_dim = max(width, height)
    scale = 1
    if max_dim > image_size:
        scale = max_dim / image_size
        new_width = int(width / scale)
        new_height = int(height / scale)
        image = cv2.resize(image, (new_width, new_height))

    return image, scale


@celery_app.task(name="analyze_sentiment")
def job(array: str):
    return asyncio.run(wdetect(array))


async def wdetect(array: str):
    file_bytes = np.array(eval(array))
    file_bytes = np.asarray(file_bytes, dtype=np.uint8)
    im1, scale = pimage(file_bytes, 640)
    lx = [2, 4, 8, 16, 32, 64, 128]
    im2 = None
    boxes, probs, classes = None, None, None
    for l1 in lx:
        file = cv2.imencode(".png", im1 if im2 is None else im2)[1].tobytes()
        encoded_image = base64.b64encode(file).decode("utf-8")
        request_data = {
            "inputs": [
                {
                    "name": "image",
                    "shape": [1],
                    "datatype": "BYTES",
                    "data": [encoded_image],
                }
            ]
        }
        response = await async_post_request(url=MLSERVER_URL, json=request_data)
        boxes = json.loads(response["outputs"][0]["data"])
        probs = json.loads(response["outputs"][1]["data"])
        classes = json.loads(response["outputs"][2]["data"])
        if (
            len(probs) > 0
            and len(boxes) > 0
            and len(classes) > 0
            and max(probs) > 0.5
            and 14 <= max(classes) <= 23
        ):
            break
        h1, w1 = im1.shape[:2]
        im2 = await decompose(im1.copy(), min(l1, w1), min(l1, h1))
    results = {
        "boxes": [[b * scale for b in box] for box in boxes],
        "probs": probs,
        "classes": classes,
    }
    return results
