import pytest


@pytest.mark.asyncio
async def test_create_short_link(client):
    test_url = "https://example.com"
    response = await client.post("/short-links", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()["data"]

    assert "shortId" in data
    assert data["url"] == test_url

    return data


@pytest.mark.asyncio
async def test_create_short_link_same_urls(client):
    test_url = "https://example.com"

    response = await client.post("/short-links", json={"url": test_url})
    assert response.status_code == 200
    data = response.json()["data"]

    assert "shortId" in data
    short_id = data["shortId"]
    assert data["url"] == test_url

    for _ in range(10):
        response = await client.post("/short-links", json={"url": test_url})
        assert response.status_code == 200
        data = response.json()["data"]
        assert short_id == data["shortId"]


@pytest.mark.asyncio
async def test_create_short_link_invalid_url(client):
    response = await client.post("/short-links", json={"url": "invalid_url"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_short_link(client):
    # url 생성
    response = await client.post("/short-links", json={"url": "https://example.com"})
    assert response.status_code == 200
    short_url = response.json()["data"]

    # 동일한 데이터가 오는지 확인
    response = await client.get(f"/short-links/{short_url['shortId']}")
    assert response.status_code == 200
    data = response.json()
    assert short_url == data["data"]


@pytest.mark.asyncio
async def test_get_unknown_short_link(client):
    response = await client.get("/short-links/unknown_id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_redirect_short_link(client):
    # url 생성
    test_url = "https://example.com"
    response = await client.post("/short-links", json={"url": test_url})
    assert response.status_code == 200
    short_url = response.json()["data"]

    # 리다이렉트확인
    response = await client.get(f"/short-links/r/{short_url['shortId']}")
    assert response.status_code == 302
    assert response.headers["Location"] == test_url


@pytest.mark.asyncio
async def test_redirect_unknown_short_link(client):
    response = await client.get("/short-links/r/unknown_id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_long_url(client):
    # 매우 긴 URL 생성
    long_url = "https://example.com/" + "a" * 10000

    # 긴 URL로 단축 URL 생성 요청
    response = await client.post("/short-links", json={"url": long_url})
    assert response.status_code == 200
    short_id = response.json()["data"]["shortId"]

    # 생성된 단축 URL로 정보 조회 요청
    get_response = await client.get(f"/short-links/{short_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["url"] == long_url

    # 생성된 단축 URL로 리다이렉트 요청 (리다이렉트는 따라가지 않음)
    redirect_response = await client.get(f"/short-links/r/{short_id}")
    assert redirect_response.status_code == 302
    assert redirect_response.headers["Location"] == long_url
