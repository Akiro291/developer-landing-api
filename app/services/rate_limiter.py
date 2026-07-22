import logging
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        self.requests_limit = 5
        self.window_seconds = 60
        self.storage_path = Path(__file__).parent.parent / 'storage' / 'rate_limit.json'
        self._ensure_storage_file()

    def _ensure_storage_file(self):
        if not self.storage_path.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)

    def _load_storage(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load rate limit storage: {e}")
            return {}

    def _save_storage(self, data: Dict[str, Any]):
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save rate limit storage: {e}")

    def _clean_old_requests(self, requests: list, current_time: float) -> list:
        return [r for r in requests if current_time - r < self.window_seconds]

    def _get_client_ip(self, client_host: str) -> str:
        return client_host or "unknown"

    async def check_rate_limit(self, client_host: str = None) -> bool:
        client_ip = self._get_client_ip(client_host)
        current_time = datetime.utcnow().timestamp()

        data = self._load_storage()
        
        if client_ip in data:
            data[client_ip] = self._clean_old_requests(data[client_ip], current_time)
            
            if len(data[client_ip]) >= self.requests_limit:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return False
            
            data[client_ip].append(current_time)
        else:
            data[client_ip] = [current_time]

        self._save_storage(data)
        return True

rate_limiter = RateLimiter()
