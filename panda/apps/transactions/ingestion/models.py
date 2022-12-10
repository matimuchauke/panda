from datetime import date, datetime

from iso3166 import countries
from pydantic import BaseModel as PydanticModel, validator


class Transaction(PydanticModel):
    date: date
    transaction_type: str
    country: str
    currency: str
    net: float
    vat: float

    @validator("date", pre=True)
    def format_date(cls, v):
        return datetime.strptime(v, "%Y/%m/%d").date()

    @validator('transaction_type')
    def validate_transaction_type(cls, v):
        condition = v.lower() in ['purchase', 'sale']
        assert condition, 'can either be Purchase or Sale'
        return v

    @validator('country')
    def validate_country(cls, v):
        try:
            return countries.get(v).alpha2
        except KeyError:
            assert False, f'Invalid country {v}'
