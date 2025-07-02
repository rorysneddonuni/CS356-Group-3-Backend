from datetime import datetime

import pytest
from httpx import AsyncClient

from app.database.tables.experiments import Experiment
from app.models.experiment import ExperimentStatus


@pytest.fixture
def experiment_input_payload():
    return {
        "ExperimentName": "IntegrationTestExp",
        "Description": "Created in test",
        "Status": "PENDING",
        "Sequences": [
            {
                "NetworkTopologyId": 1,
                "NetworkDisruptionProfileId": 1,
                "EncodingParameters": {"codec": "h264"}
            }
        ]
    }


@pytest.mark.asyncio
class TestExperimentsRoutes:

    async def test_create_experiment_success(self, async_client: AsyncClient, experiment_input_payload):
        response = await async_client.post("/experiments", json=experiment_input_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["ExperimentName"] == experiment_input_payload["ExperimentName"]
        assert data["status"] == "PENDING"
        assert len(data["Sequences"]) == 1

    async def test_create_duplicate_experiment_name(self, async_client: AsyncClient, experiment_input_payload):
        await async_client.post("/experiments", json=experiment_input_payload)

        response = await async_client.post("/experiments", json=experiment_input_payload)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    async def test_get_experiment_by_id(self, async_client: AsyncClient, experiment_input_payload):
        create_resp = await async_client.post("/experiments", json=experiment_input_payload)
        exp_id = create_resp.json()["Id"]

        response = await async_client.get(f"/experiments/{exp_id}")
        assert response.status_code == 200
        assert response.json()["Id"] == exp_id

    async def test_update_experiment_fields(self, async_client: AsyncClient, experiment_input_payload):
        create_resp = await async_client.post("/experiments", json=experiment_input_payload)
        exp_id = create_resp.json()["Id"]

        update_payload = {
            "ExperimentName": "Updated Name",
            "Description": "New Desc",
            "Status": "COMPLETE",
            "AddSequences": [],
            "RemoveSequenceIds": []
        }

        update_resp = await async_client.put(f"/experiments/{exp_id}", json=update_payload)
        assert update_resp.status_code == 200
        assert update_resp.json()["ExperimentName"] == "Updated Name"
        assert update_resp.json()["status"] == "COMPLETE"

    async def test_delete_experiment(self, async_client: AsyncClient, db):
        experiment = Experiment(
            experiment_name="ToDelete",
            description="Should be deleted",
            owner_id=1,
            status=ExperimentStatus.PENDING,
            created_at=datetime.now().isoformat(),
        )

        db.add(experiment)
        await db.commit()
        await db.refresh(experiment)

        response = await async_client.delete(f"/experiments/{experiment.id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Experiment deleted"

        assert await db.get(Experiment, experiment.id) is None
