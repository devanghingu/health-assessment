import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ValidationError


class ClaimFileModel(BaseModel):

    service_date: datetime = Field(..., alias="service date")
    submitted_procedure: str = Field(..., alias="submitted procedure")
    quadrant: str
    plan_group: str = Field(..., alias="Plan/Group #")
    subscriber: str = Field(..., alias="Subscriber#")
    provider_npi: str = Field(..., alias="Provider NPI")
    provider_fees: float = Field(..., alias="provider fees")
    allowed_fees: float = Field(..., alias="Allowed fees")
    member_coinsurance: float = Field(..., alias="member coinsurance")
    member_copay: float = Field(..., alias="member copay")

    @field_validator("provider_npi")
    @classmethod
    def validate_provider_npi(cls, value):
        """Ensure Provider NPI is exactly 10 digits."""
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Provider NPI must be exactly 10 digits.")
        return value

    @field_validator("submitted_procedure")
    @classmethod
    def validate_submitted_procedure(cls, value):
        """ Validate 'submitted procedure' always start with char 'D' """
        if not value.startswith("D"):
            raise ValueError("submitted Procedure must start with 'D'.")
        return value

    @field_validator("service_date", mode="before")
    @classmethod
    def validate_date(cls, value):
        """ validate datetime format for service date"""
        try:
            value = datetime.strptime(value, "%m/%d/%y %H:%M")
        except (TypeError,ValueError):
            raise ValidationError("service date field must be datetime.")
        return value

    @field_validator("provider_fees", "allowed_fees", "member_coinsurance", "member_copay", mode="before")
    @classmethod
    def validate_dollar_amount(cls, value):
        """validate Remove dollar signs and convert to float. here float class raise value error by itself"""
        return float(re.sub(r"[^\d.]", "", value)) if value else 0.0

    class Config:
        populate_by_name = True
        from_attributes = True