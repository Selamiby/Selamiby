"""
Asynchronous işlemler - CPU verimli çalışma
"""

import asyncio
import aiohttp
from typing import List, Optional, Callable, Any
from functools import wraps
import time


class AsyncBatchProcessor:
    """Batch işleme - CPU dostu"""
    
    def __init__(self, batch_size: int = 10, delay: float = 0.01):
        self.batch_size = batch_size
        self.delay = delay
    
    async def process(self, items: List[Any], func: Callable) -> List[Any]:
        """Batch'ler halinde işle"""
        results = []
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_results = await asyncio.gather(*[func(item) for item in batch])
            results.extend(batch_results)
            await asyncio.sleep(self.delay)  # CPU relax
        return results


class AsyncHTTPClient:
    """Hafif async HTTP client"""
    
    def __init__(self, timeout: int = 10, max_connections: int = 5):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.connector = aiohttp.TCPConnector(limit=max_connections)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, **kwargs) -> str:
        """GET isteği yap"""
        if not self.session:
            raise RuntimeError("Session başlatılmamış")
        async with self.session.get(url, **kwargs) as response:
            return await response.text()
    
    async def post(self, url: str, **kwargs) -> str:
        """POST isteği yap"""
        if not self.session:
            raise RuntimeError("Session başlatılmamış")
        async with self.session.post(url, **kwargs) as response:
            return await response.text()


class RateLimiter:
    """Rate limiting - güvenli API kullanımı"""
    
    def __init__(self, max_calls: int = 10, time_window: float = 1.0):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    async def wait(self):
        """Rate limit uygulaması"""
        now = time.time()
        self.calls = [call for call in self.calls if now - call < self.time_window]
        
        if len(self.calls) >= self.max_calls:
            sleep_time = self.time_window - (now - self.calls[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.calls.append(now)


def async_retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry dekoratörü async fonksiyonlar için"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator


async def run_async_tasks(tasks: List, max_concurrent: int = 5) -> List:
    """Async taskları kontrollü şekilde çalıştır"""
    results = []
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def bounded_task(task):
        async with semaphore:
            return await task
    
    for task in tasks:
        results.append(await bounded_task(task))
    
    return results
