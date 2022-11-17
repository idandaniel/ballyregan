from pydantic import BaseModel


class HashableBaseModel(BaseModel):
    
    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))