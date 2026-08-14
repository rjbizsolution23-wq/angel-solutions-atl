"""
Prometheus Archive Engine - Token Bucket Rate Limiter
Prevents API overload and restricts free/pro/enterprise resource quotas
Supports Redis and falls back to local memory storage
"""
import time
import os
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status

# Retrieve Redis configuration options
REDIS_URL = os.getenv("REDIS_URL", "")

# Local fallback store for rate limits in case Redis is disabled
# Maps key -> (tokens, last_update_time)
_LOCAL_LIMITS_STORE: Dict[str, Tuple[float, float]] = {}

# Tiers Configuration (Capacity, Fill Rate per second)
TIER_LIMITS = {
    "unauthenticated": (3, 3 / 60.0), # Cap 3 requests, regens 3/min
    "free": (10, 10 / 60.0),          # Cap 10 requests, regens 10/min
    "pro": (200, 200 / 60.0),         # Cap 200 requests, regens 200/min
    "enterprise": (1000, 1000 / 60.0) # Cap 1000 requests, regens 1000/min
}

class TokenBucketRateLimiter:
    """Token Bucket rate limiting engine"""
    
    def __init__(self):
        self.redis_client = None
        if REDIS_URL:
            try:
                import redis
                self.redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            except ImportError:
                pass

    def check_rate_limit(self, key_prefix: str, tier: str) -> None:
        """Enforces token bucket evaluation. Throws HTTP 429 if depleted."""
        capacity, fill_rate = TIER_LIMITS.get(tier, TIER_LIMITS["unauthenticated"])
        now = time.time()
        key = f"rate_limit:{key_prefix}"

        if self.redis_client:
            # Redis rate limit implementation
            try:
                # Retrieve existing state
                state = self.redis_client.hmget(key, ["tokens", "last_updated"])
                if state[0] is not None and state[1] is not None:
                    tokens = float(state[0])
                    last_updated = float(state[1])
                    # Add newly generated tokens
                    delta = now - last_updated
                    tokens = min(capacity, tokens + (delta * fill_rate))
                else:
                    tokens = float(capacity)

                if tokens < 1.0:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Please back off or upgrade subscription."
                    )

                # Consume 1 token
                tokens -= 1.0
                self.redis_client.hset(key, mapping={"tokens": str(tokens), "last_updated": str(now)})
                # Set TTL to 1 hour to prevent memory leaks
                self.redis_client.expire(key, 3600)
                return
            except Exception:
                # Redis failure fallback to memory
                pass

        # Local Memory fallback implementation
        global _LOCAL_LIMITS_STORE
        if key in _LOCAL_LIMITS_STORE:
            tokens, last_updated = _LOCAL_LIMITS_STORE[key]
            delta = now - last_updated
            tokens = min(capacity, tokens + (delta * fill_rate))
        else:
            tokens = float(capacity)

        if tokens < 1.0:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please back off or upgrade subscription."
            )

        tokens -= 1.0
        _LOCAL_LIMITS_STORE[key] = (tokens, now)

# Create singleton global instance
limiter = TokenBucketRateLimiter()

async def rate_limit_dependency(request: Request) -> None:
    """FastAPI global router dependency wrapper"""
    # Check if authorization bearer or session context exists
    auth_header = request.headers.get("Authorization")
    
    tier = "unauthenticated"
    identifier = request.client.host if request.client else "unknown_ip"
    
    if auth_header and auth_header.startswith("Bearer "):
        # Inspect active token to infer subscription tier without DB hitting
        try:
            from .auth import decode_token
            payload = decode_token(auth_header.split(" ")[1])
            identifier = payload.get("sub", identifier)
            tier = payload.get("tier", "free")
        except Exception:
            pass

    limiter.check_rate_limit(f"{tier}:{identifier}", tier)
