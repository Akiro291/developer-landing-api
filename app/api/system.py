from fastapi import APIRouter
from app.services.metrics_service import metrics_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "ok"}

@router.get("/metrics")
async def get_metrics():
    return metrics_service.get_metrics()

@router.post("/metrics/reset")
async def reset_metrics():
    metrics_service.reset_metrics()
    return {"message": "Metrics reset successfully"}
