from typing import ClassVar
from typing import List, Optional, Tuple, Union

from pydantic import StrictBytes, StrictStr

from app.models.video import Video


class VideosService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        VideosService.subclasses = VideosService.subclasses + (cls,)

    async def create_video(self, video: Optional[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]],
                           frame_rate: Optional[StrictStr], resolution: Optional[StrictStr], ) -> Video:
        """Upload a new video to the infrastructure portal (Super User access required)."""
        ...

    async def delete_video(self, id: StrictStr, ) -> Video:
        """Delete a specific video by ID (Super User access required)."""
        ...

    async def get_video(self, id: StrictStr, ) -> Video:
        """Fetch a specific video by ID."""
        ...

    async def get_videos(self, ) -> List[Video]:
        """Fetch a list of all available videos."""
        ...
