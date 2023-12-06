import asyncio
import random

import pytest

from src.services.short_url_service import ShortUrlService


@pytest.mark.asyncio
async def test_controlling_concurrency_to_generate_unique_short_ids(db, redis_cache):
    async for session in db:
        service = ShortUrlService(session, redis_cache)
        generated_ids = set()

        # pseudo를 랜덤값으로 초기화
        pseudo = random.randint(0, 10**10)
        redis_cache.set(service.pkey, pseudo)

        async def func(idx):
            for i in range(1000 * idx, 1000 * (idx + 1)):
                short_id = service._generate_short_id()
                generated_ids.add(short_id)

        await asyncio.gather(*[func(i) for i in range(8)])

        assert len(generated_ids) == 1000 * 8
