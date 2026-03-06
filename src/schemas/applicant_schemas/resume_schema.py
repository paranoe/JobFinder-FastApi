from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from src.schemas.profession_schema import ProfessionResponse
from src.schemas.skill_schema import SkillResponse
from src.schemas.applicant_schemas.work_experience_schema import WorkExperienceResponse

class ResumeBase(BaseModel):
    profession_id: int = Field(..., example=1)

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    applicant_id: int
    profession: Optional[ProfessionResponse] = None
    skills: List[SkillResponse] = []
    work_experiences: List[WorkExperienceResponse] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "profession_id": 1,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-02-20T14:25:00",
                "applicant_id": 1,
                "profession": {"id": 1, "name": "Python разработчик"},
                "skills": [{"id": 1, "name": "FastAPI"}, {"id": 2, "name": "PostgreSQL"}],
                "work_experiences": [
                    {
                        "id": 1,
                        "resume_id": 1,
                        "company_name": "Яндекс",
                        "position": "Python Developer",
                        "start_date": "2020-07-01",
                        "end_date": "2023-12-31",
                        "description": "Разработка API"
                    }
                ]
            }
        }
    }