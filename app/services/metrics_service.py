import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MetricsService:
    def __init__(self):
        self.storage_path = Path(__file__).parent.parent / 'storage' / 'metrics.json'
        self._ensure_storage_file()

    def _ensure_storage_file(self):
        if not self.storage_path.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump({
                    "total_requests": 0,
                    "successful_ai_requests": 0,
                    "failed_requests": 0,
                    "last_updated": None
                }, f)

    def _load_metrics(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load metrics: {e}")
            return {
                "total_requests": 0,
                "successful_ai_requests": 0,
                "failed_requests": 0,
                "last_updated": None
            }

    def _save_metrics(self, data: Dict[str, Any]):
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save metrics: {e}")

    def record_request(self, success: bool = True, ai_processed: bool = False):
        data = self._load_metrics()
        
        data["total_requests"] = data.get("total_requests", 0) + 1
        
        if ai_processed:
            data["successful_ai_requests"] = data.get("successful_ai_requests", 0) + 1
        
        if not success:
            data["failed_requests"] = data.get("failed_requests", 0) + 1
        
        data["last_updated"] = datetime.utcnow().isoformat()
        
        self._save_metrics(data)

    def get_metrics(self) -> Dict[str, Any]:
        return self._load_metrics()

    def reset_metrics(self):
        data = {
            "total_requests": 0,
            "successful_ai_requests": 0,
            "failed_requests": 0,
            "last_updated": datetime.utcnow().isoformat()
        }
        self._save_metrics(data)

metrics_service = MetricsService()
