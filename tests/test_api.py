from custom_components.kronprins_frederiks_bro.api import MyIntegrationApiClient


async def test_async_get_status_returns_expected_shape():
    client = MyIntegrationApiClient(host="127.0.0.1")

    result = await client.async_get_status()

    assert result["status"] == "ok"
    assert result["host"] == "127.0.0.1"
