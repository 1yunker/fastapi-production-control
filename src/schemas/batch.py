from pydantic import BaseModel, ConfigDict


class BatchRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pass
