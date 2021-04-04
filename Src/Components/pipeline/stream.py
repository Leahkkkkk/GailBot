# Standard library imports
from typing import Any
# Local imports
from ...utils.models import IDictModel
# Third party imports

class Stream(IDictModel):

    def __init__(self, data : Any) -> None:
        super().__init__()
        self.set("data",data)

