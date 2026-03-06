from pydantic import BaseModel, Field

class CityBase(BaseModel):
    name: str = Field(..., example="Москва", min_length=2, max_length=100)

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Москва"
            }
        }
    }