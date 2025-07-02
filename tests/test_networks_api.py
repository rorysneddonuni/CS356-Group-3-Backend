import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestNetworksRoutes:

    async def test_create_network_success(self, async_client: AsyncClient, test_network_json):
        response = await async_client.post("/infrastructure/networks", json=test_network_json)

        assert response.status_code == 201
        data = response.json()

        assert data["networkName"] == test_network_json["networkName"]
        assert data["packetLoss"] == test_network_json["packetLoss"]

    async def test_get_network_by_id(self, async_client: AsyncClient, network_factory, test_network_json):
        created = await network_factory(test_network_json)

        response = await async_client.get(f"/infrastructure/networks/{created.network_profile_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["networkName"] == test_network_json["networkName"]
        assert data["delay"] == test_network_json["delay"]

    async def test_update_network(self, async_client: AsyncClient, network_factory, test_network_json):
        created = await network_factory(test_network_json)

        updated_json = test_network_json.copy()
        updated_json["description"] = "Updated description"
        updated_json["delay"] = 99

        response = await async_client.put(
            f"/infrastructure/networks/{created.network_profile_id}",
            json=updated_json
        )

        assert response.status_code == 200
        data = response.json()

        assert data["description"] == "Updated description"
        assert data["delay"] == 99

    async def test_delete_network(self, async_client: AsyncClient, network_factory, test_network_json):
        created = await network_factory(test_network_json)

        response = await async_client.delete(f"/infrastructure/networks/{created.network_profile_id}")

        assert response.status_code == 200
        assert "message" in response.json()

    async def test_get_networks_list(self, async_client: AsyncClient):
        response = await async_client.get("/infrastructure/networks")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
