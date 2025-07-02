import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestEncodersRoutes:

    async def test_create_encoder_success(self, async_client: AsyncClient, test_encoder_json):
        response = await async_client.post("/infrastructure/encoders", json=test_encoder_json)

        assert response.status_code == 200
        assert response.json()["message"] == "Encoder created successfully"

    async def test_get_encoder_by_id(self, async_client: AsyncClient, encoder_factory, test_encoder_json):
        await encoder_factory(test_encoder_json)

        response = await async_client.get(f"/infrastructure/encoders/{test_encoder_json['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == test_encoder_json["name"]

    async def test_update_encoder(self, async_client: AsyncClient, encoder_factory, test_encoder_json):
        await encoder_factory(test_encoder_json)

        updated_data = test_encoder_json.copy()
        updated_data["comment"] = "Updated encoder comment"
        updated_data["noOfLayers"] = 2

        response = await async_client.put(f"/infrastructure/encoders/{test_encoder_json['id']}", json=updated_data)

        assert response.status_code == 200
        assert "updated successfully" in response.json()["message"]

    async def test_delete_encoder(self, async_client: AsyncClient, encoder_factory, test_encoder_json):
        await encoder_factory(test_encoder_json)

        response = await async_client.delete(f"/infrastructure/encoders/{test_encoder_json['id']}")
        assert response.status_code == 200
        assert response.json()["message"] == "Encoder deleted"

    async def test_get_encoders_list(self, async_client: AsyncClient):
        response = await async_client.get("/infrastructure/encoders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
