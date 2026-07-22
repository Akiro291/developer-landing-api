from fastapi import Request, HTTPException, status
import time

async def rate_limit_middleware(request: Request, call_next):
    from app.services.rate_limiter import rate_limiter
    
    if not await rate_limiter.check_rate_limit(request):
        remaining_time = 60
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {remaining_time} seconds."
        )
    
    response = await call_next(request)
    return response
