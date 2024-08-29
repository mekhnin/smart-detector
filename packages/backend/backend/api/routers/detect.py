from backend.schemas.requests import ArrayModel
from backend.services.utils import print_logger_info
from celery import Celery
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


celery_app = Celery(
    "tasks", backend="redis://redis", broker="pyamqp://guest:guest@rabbitmq//"
)


@router.post("/detect/")
async def detect(request: ArrayModel, background_tasks: BackgroundTasks):
    """
    Animal detection endpoint.
    """
    async_result = celery_app.send_task("analyze_sentiment", args=[request.array])
    background_tasks.add_task(
        print_logger_info,
        hash(request.array),
        async_result.get(),
    )
    return async_result.get()
