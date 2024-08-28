import asyncio
import base64
import json
from io import BytesIO

import aiohttp
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib import patches
from PIL import Image

BACKEND_URL: str = "http://backend:5000/api/detect/"
CLASS_LABELS = {
    14: "Bird",
    15: "Cat",
    16: "Dog",
    17: "Horse",
    18: "Sheep",
    19: "Cow",
    20: "Elephant",
    21: "Bear",
    22: "Zebra",
    23: "Giraffe",
}


async def async_post_request(url, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json) as response:
            return await response.json()


async def async_post_request_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()


def encode_image_to_base64(image_path):
    """
    Кодирует изображение в строку Base64.

    :param image_path: Путь к файлу изображения.
    :return: Строка, закодированная в Base64.
    """
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded


def send_image_to_mlserver(image_path, url):
    """
    Отправляет POST запрос на MLServer с изображением в формате Base64.

    :param image_path: Путь к файлу изображения.
    :param url: URL MLServer для обработки запросов.
    :return: Ответ сервера.
    """
    encoded_image = encode_image_to_base64(image_path)

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
    return async_post_request(url, request_data)


def main():
    with st.form(key="image_form"):
        st.write("Upload an image file")
        uploaded_file = st.file_uploader(
            "Choose an image...", type=["jpg", "png", "jpeg"]
        )
        submitted = st.form_submit_button("Submit")
    if submitted and uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        array_str = json.dumps(file_bytes.tolist())
        response = asyncio.run(
            async_post_request(url=BACKEND_URL, json={"array": array_str})
        )
        if "error" in response:
            st.text(response["error"])
        else:
            boxes = response["boxes"]
            probs = response["probs"]
            classes = response["classes"]
            img = Image.open(BytesIO(file_bytes))
            if img.mode == "L" or img.mode == "LA":
                img = img.convert("RGB")
            fig, ax = plt.subplots()

            ax.imshow(img)

            for box, prob, cls in zip(boxes, probs, classes):
                if prob <= 0.5:
                    continue
                x, y, w, h = [b for b in box]
                rect = patches.Rectangle(
                    (x - w / 2, y - h / 2),
                    w,
                    h,
                    linewidth=2,
                    edgecolor="r",
                    facecolor="none",
                )
                ax.add_patch(rect)
                label = f"{CLASS_LABELS[int(cls)]}: {prob:.2f}"
                plt.text(
                    x - w / 2,
                    y - h / 2,
                    label,
                    color="white",
                    fontsize=12,
                    bbox=dict(facecolor="red", alpha=0.5),
                )

            plt.show()

            st.write("Uploaded Image:")
            st.pyplot(fig)


if __name__ == "__main__":
    st.title("Smart Animal Detector")
    main()
