from typing import ClassVar
from typing import List, Optional, Tuple, Union

from pydantic import Field, StrictBytes, StrictStr
from typing_extensions import Annotated

from app.models.experiment import Experiment
from app.models.experiment_input import ExperimentInput
from app.models.experiment_status import ExperimentStatus


class ExperimentsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ExperimentsService.subclasses = ExperimentsService.subclasses + (cls,)

    async def create_experiment(self, experiment_input: Annotated[Optional[ExperimentInput], Field(
        description="Experiment object that needs to be added to the store")], ) -> Experiment:
        """Create a new experiment under a given user."""
        ...

    async def delete_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], ) -> None:
        """Delete an experiment."""
        ...

    async def get_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], ) -> Experiment:
        """Get full details of an experiment by its unique ID."""
        ...

    async def get_experiment_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], ) -> None:
        """Get list of files to download for results."""
        ...

    async def get_experiment_status(self, experiment_id: Annotated[
        StrictStr, Field(description="Unique ID to identify the experiment.")], ) -> ExperimentStatus:
        """Retrieve the current status and progress of an experiment."""
        ...

    async def get_experiments(self, ) -> Experiment:
        """List experiments for a given user."""
        ...

    async def update_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], experiment_input: Annotated[
        Optional[ExperimentInput], Field(
            description="Experiment object that needs to be added to the store")], ) -> None:
        """This can only be done by the user who owns the experiment."""
        ...

    async def upload_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], filename: Optional[
        List[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]]], ) -> None:
        """This can only be done by the logged in user."""
        ...
