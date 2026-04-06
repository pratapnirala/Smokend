from pydantic import BaseModel, model_validator
from typing import Optional


class Achievement(BaseModel):
    not_smoked: Optional[bool] = False
    go_for_run: Optional[bool] = False
    finished_book: Optional[bool] = False
    notes: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_selected(cls, values):
        if not (values.not_smoked or values.go_for_run or values.finished_book):
            raise ValueError("At least one activity must be selected")
        return values
