from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

class EducationBase(BaseModel):
    institution_name: str = Field(..., example="МГУ им. Ломоносова", min_length=2, max_length=200)
    start_date: date = Field(..., example="2015-09-01")
    end_date: Optional[date] = Field(None, example="2020-06-30")

    @field_validator('end_date')
    def validate_dates(cls, v, values):
        if v and values.data.get('start_date') and v < values.data['start_date']:
            raise ValueError('Дата окончания не может быть раньше даты начала')
        return v

class EducationCreate(EducationBase):
    pass

class EducationUpdate(EducationBase):
    pass

class EducationResponse(EducationBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "institution_name": "МГУ им. Ломоносова",
                "start_date": "2015-09-01",
                "end_date": "2020-06-30"
            }
        }
    }