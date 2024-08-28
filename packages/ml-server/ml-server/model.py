import base64
import json
from io import BytesIO

import mlserver as ms
import numpy as np
from mlserver import MLModel, ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput
from PIL import Image
from ultralytics import YOLO


def serialize_numpy(np_array):
    return json.dumps(np.array(np_array).tolist())


def base64_to_img(b64str):
    image_data = base64.b64decode(b64str)
    image = Image.open(BytesIO(image_data))
    image = image.convert("RGB")
    return np.array(image)


class YOLOv10Model(MLModel):
    def __init__(self, settings: ModelSettings):
        super().__init__(settings)
        self._model = None

    async def load(self) -> bool:
        self._model = YOLO("yolov10n.pt")
        ms.register("count_obj_detection", "This is a count objects detection")
        return await super().load()

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        img = base64_to_img(payload.inputs[0].data[0])
        results = self._model(img)
        response_outputs = []

        for result in results:
            response_outputs.append(
                ResponseOutput(
                    name="boxes",
                    shape=result.boxes.xywh.shape,
                    datatype="FP32",
                    data=serialize_numpy(result.boxes.xywh),
                )
            )
            response_outputs.append(
                ResponseOutput(
                    name="probs",
                    shape=result.boxes.conf.shape,
                    datatype="FP32",
                    data=serialize_numpy(result.boxes.conf),
                )
            )
            response_outputs.append(
                ResponseOutput(
                    name="cls",
                    shape=result.boxes.cls.shape,
                    datatype="FP32",
                    data=serialize_numpy(result.boxes.cls),
                )
            )
        ms.log(count_obj_detection=len(response_outputs))
        return InferenceResponse(
            model_name="yolov10n", model_version="v1", outputs=response_outputs
        )
