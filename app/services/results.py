from typing import ClassVar
from typing import List, Optional, Tuple, Union

from pydantic import Field, StrictBytes, StrictStr
from typing_extensions import Annotated


class ResultsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ResultsService.subclasses = ResultsService.subclasses + (cls,)

    async def get_experiment_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], ) -> None:
        """Get list of files to download for results."""
        ...

    async def upload_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], filename: Optional[
        List[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]]], ) -> None:
        """This can only be done by the logged-in user."""
        ...
