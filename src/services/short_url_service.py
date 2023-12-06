import hashlib
from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy import select

from src import models
from src.modules.cache import CacheDepends, RedlockManager
from src.modules.database import AsyncSessionDepends


def _next_pseudo(p: int) -> int:
    # generate random value by previous pseudo value
    # REFERENCE : https://en.wikipedia.org/wiki/Linear_congruential_generator
    multiple_factor = 6538825
    plus_factor = 742581238909
    mod_factor = 2821109907456
    return (p * multiple_factor + plus_factor) % mod_factor


class ShortUrlService:
    pkey = "pseudo"
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    def __init__(self, session: AsyncSessionDepends, cache: CacheDepends):
        self.session = session
        self.cache = cache
        self.dlm = RedlockManager(cache)

    @staticmethod
    def _next_pseudo(p: int) -> int:
        # generate random value by previous pseudo value
        # REFERENCE : https://en.wikipedia.org/wiki/Linear_congruential_generator
        multiple_factor = 6538825
        plus_factor = 742581238909
        mod_factor = 2821109907456
        return (p * multiple_factor + plus_factor) % mod_factor

    def _get_minimum_size(self) -> int:
        # 10억개의 short_link 를 만들기 위한 최소 길이
        import math

        return math.ceil(math.log(10**10, len(self.chars)))  # 결과는 6

    @property
    def _minimum_size(self) -> int:
        # _get_minimum_size 의 결과
        return 6

    def _to_code(self, p: int):
        code = ""

        while p != 0 and len(code) < self._minimum_size:
            ch = self.chars[int(p % len(self.chars))]
            code = ch + code
            p = int(p / len(self.chars))

        code = "a" * (self._minimum_size - len(code)) + code
        return code

    def _get_pseudo(self) -> int:
        lock = self.dlm.get_lock(self.pkey)
        pseudo = int(self.cache.get(self.pkey) or 0)
        pseudo = self._next_pseudo(pseudo)
        self.cache.set(self.pkey, pseudo)
        self.dlm.unlock(lock)
        return pseudo

    def _generate_short_id(self) -> str:
        pseudo = self._get_pseudo()
        return self._to_code(pseudo)

    @staticmethod
    def _url_to_hash(url_str: str) -> str:
        parsed_url = urlparse(url_str)
        url_dict = dict(
            schema=parsed_url.scheme,
            hostname=parsed_url.hostname,
            port=parsed_url.port,
            path=parsed_url.path,
            query=parsed_url.query,
            fragment=parsed_url.fragment,
            params=parsed_url.params,
        )
        return hashlib.md5(repr(url_dict).encode()).hexdigest()

    async def get(self, short_id: str) -> models.ShortUrl | None:
        return await self.session.scalar(
            select(models.ShortUrl).where(models.ShortUrl.short_id == short_id)
        )

    def create(self, url_str: str) -> models.ShortUrl:
        result = models.ShortUrl(
            short_id=self._generate_short_id(),
            url_str=url_str,
            url_hash=self._url_to_hash(url_str),
            created_at=datetime.utcnow(),
        )
        self.session.add(result)
        return result

    async def find_exist(self, url_str: str) -> models.ShortUrl | None:
        return await self.session.scalar(
            select(models.ShortUrl).where(
                models.ShortUrl.url_hash == self._url_to_hash(url_str)
            )
        )
