import re

from fastapi import HTTPException


def is_url(url_str: str) -> bool:

    # URL 패턴을 정의합니다.
    url_pattern = re.compile(
        r"^(https?://"  # 스킴 (http 또는 https) - 필수
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # 도메인 이름
        r"localhost|"  # 또는 localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # 또는 IP 주소
        r"(?::\d+)?"  # 포트 (선택 사항)
        r"(?:/?|[/?]\S+)$)",  # 경로 및 쿼리 문자열 (선택 사항)
        re.IGNORECASE,
    )
    return bool(re.match(url_pattern, url_str))


def is_url_or_raise(url_str: str):
    if not is_url(url_str):
        raise HTTPException(status_code=400, detail="Invalid url")
