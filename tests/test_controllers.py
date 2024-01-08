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
async def test_create_short_link_invalid_url(client):
    response = await client.post("/short-links", json={"url": "invalid_url"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_short_link(client):
    # generate url
    response = await client.post("/short-links", json={"url": "https://example.com"})
    assert response.status_code == 200
    short_url = response.json()["data"]

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
    test_url = "https://example.com"
    response = await client.post("/short-links", json={"url": test_url})
    assert response.status_code == 200
    short_url = response.json()["data"]

    response = await client.get(f"/short-links/r/{short_url['shortId']}")
    assert response.status_code == 302
    assert response.headers["Location"] == test_url


@pytest.mark.asyncio
async def test_redirect_unknown_short_link(client):
    response = await client.get("/short-links/r/unknown_id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_long_url(client):
    # long url
    long_url = "https://example.com/" + "a" * 10000

    response = await client.post("/short-links", json={"url": long_url})
    assert response.status_code == 200
    short_id = response.json()["data"]["shortId"]

    get_response = await client.get(f"/short-links/{short_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["url"] == long_url

    redirect_response = await client.get(f"/short-links/r/{short_id}")
    assert redirect_response.status_code == 302
    assert redirect_response.headers["Location"] == long_url
