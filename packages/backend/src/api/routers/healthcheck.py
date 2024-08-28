from backend.schemas.healthcheck import HealthcheckResult
from backend.services.utils import return_current_time
from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck/", name="healthcheck", response_model=HealthcheckResult)
def get_health_check() -> HealthcheckResult:
    """
    Healthcheck endpoint
    """
    health_check = HealthcheckResult(is_alive=True, date=return_current_time())

    return health_check
