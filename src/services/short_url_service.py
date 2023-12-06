from src import models
from src.modules.cache import CacheDepends
from src.modules.database import AsyncSessionDepends


class ShortUrlService:
    pkey = "pseudo"
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    def __init__(self, session: AsyncSessionDepends, cache: CacheDepends):
        self.session = session
        self.cache = cache

    @staticmethod
    def _next_pseudo(p: int) -> int:
        # generate random value by previous pseudo value
        # REFERENCE : https://en.wikipedia.org/wiki/Linear_congruential_generator
        multiple_factor = 6538825
        plus_factor = 742581238909
        mod_factor = 2821109907456
        return (p * multiple_factor + plus_factor) % mod_factor

    @property
    def minimum_size(self) -> int:
        # 10억개의 short_link 를 만들기 위한 최소 길이
        import math

        return math.ceil(math.log(10**10, len(self.chars)))  # 결과는 6

    def _to_code(self, p: int):
        code = ""

        while p != 0 and len(code) < 6:
            ch = self.chars[int(p % len(self.chars))]
            code = ch + code
            p = int(p / len(self.chars))

        code = "a" * (6 - len(code)) + code
        return code

    async def _generate_short_id(self) -> str:
        cache = self.cache
        pseudo = int(await cache.getset(self.pkey, 0))

        pseudo = self._next_pseudo(pseudo)
        await cache.set(self.pkey, pseudo)
        return self._to_code(pseudo)

    async def get(self, short_id: str) -> models.ShortUrl | None:
        return await self.session.get(
            models.ShortUrl, models.ShortUrl.short_id == short_id
        )

    async def create(self, url: str) -> models.ShortUrl:
        pass
