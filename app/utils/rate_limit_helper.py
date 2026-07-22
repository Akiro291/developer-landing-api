import json
import time
from pathlib import Path
from typing import List, Dict

def load_rate_limit_storage() -> Dict:
    try:
        with open("storage/rate_limit.json", 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"requests": {}}

def save_rate_limit_storage(data: Dict):
    with open("storage/rate_limit.json", 'w') as f:
        json.dump(data, f, indent=2)

def check_rate_limit(ip: str, max_requests: int = 5, window_seconds: int = 60) -> bool:
    data = load_rate_limit_storage()
    current_time = time.time()
    
    if ip not in data:
        data[ip] = []
    
    data[ip] = [t for t in data[ip] if current_time - t < window_seconds]
    
    if len(data[ip]) >= max_requests:
        return False
    
    data[ip].append(current_time)
    save_rate_limit_storage(data)
    return True
