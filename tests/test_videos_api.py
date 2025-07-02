import pytest
import io
import uuid
from httpx import AsyncClient


@pytest.mark.asyncio
class TestVideosRoutes:

    async def test_create_video_success(self, async_client: AsyncClient, test_video_data):
        file = io.BytesIO(b"YUV4MPEG2 dummy content")

        response = await async_client.post(
            "/infrastructure/videos",
            data=test_video_data,
            files={"video_file": ("video.y4m", file, "video/x-yuv4mpeg")}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == test_video_data["title"]
        assert data["format"] == test_video_data["format"]

    async def test_create_video_invalid_bit_depth(self, async_client: AsyncClient, test_video_data):
        bad_data = test_video_data.copy()
        bad_data["bitDepth"] = 12  # Invalid

        file = io.BytesIO(b"dummy")

        response = await async_client.post(
            "/infrastructure/videos",
            data=bad_data,
            files={"video_file": ("video.y4m", file, "video/x-yuv4mpeg")}
        )

        assert response.status_code == 400
        assert "bitdepth must be either 8 or 10" in response.text.lower()

    async def test_create_video_invalid_resolution(self, async_client: AsyncClient, test_video_data):
        bad_data = test_video_data.copy()
        bad_data["resolution"] = "badformat"

        file = io.BytesIO(b"dummy")

        response = await async_client.post(
            "/infrastructure/videos",
            data=bad_data,
            files={"video_file": ("video.y4m", file, "video/x-yuv4mpeg")}
        )

        assert response.status_code == 400
        assert "resolution must follow the format" in response.text.lower()

    async def test_get_video_by_id(self, async_client: AsyncClient, video_factory, test_video_data):
        created = await video_factory(**test_video_data)

        response = await async_client.get(f"/infrastructure/videos/{created.id}")

        assert response.status_code == 200
        assert response.headers["content-type"] in ["video/x-yuv4mpeg", "application/octet-stream"]

    async def test_get_videos_list(self, async_client: AsyncClient):
        response = await async_client.get("/infrastructure/videos")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_delete_video(self, async_client: AsyncClient, video_factory, test_video_data):
        created = await video_factory(**test_video_data)

        response = await async_client.delete(f"/infrastructure/videos/{created.id}")

        assert response.status_code == 200
        assert response.json()["message"] == "Video deleted"

    async def test_get_nonexistent_video(self, async_client: AsyncClient):
        response = await async_client.get(f"/infrastructure/videos/{uuid.uuid4()}")

        assert response.status_code == 404

    async def test_delete_nonexistent_video(self, async_client: AsyncClient):
        response = await async_client.delete(f"/infrastructure/videos/{uuid.uuid4()}")

        assert response.status_code == 404
