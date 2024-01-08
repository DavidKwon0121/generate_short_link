import asyncio
import random

import pytest

from src.services.short_link_service import ShortLinkService


@pytest.mark.asyncio
async def test_is_alphanumeric(session, cache):
    service = ShortLinkService(session, cache)

    # initiate pseudo as a random value
    pseudo = random.randint(0, 10**10)
    cache.set(service.pkey, pseudo)

    for i in range(500):
        short_id = service._generate_short_id()
        assert short_id.isalnum()


@pytest.mark.asyncio
async def test_controlling_concurrency_to_generate_unique_short_ids(session, cache):
    service = ShortLinkService(session, cache)
    generated_ids = set()

    # initiate pseudo as a random value
    pseudo = random.randint(0, 10**10)
    cache.set(service.pkey, pseudo)

    async def func(idx):
        for i in range(300 * idx, 300 * (idx + 1)):
            short_id = service._generate_short_id()
            generated_ids.add(short_id)

    await asyncio.gather(*[func(i) for i in range(8)])

    assert len(generated_ids) == 300 * 8
