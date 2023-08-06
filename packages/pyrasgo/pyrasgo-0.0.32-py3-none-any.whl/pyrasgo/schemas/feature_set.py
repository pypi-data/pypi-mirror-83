from typing import Optional
from pydantic import BaseModel

from pyrasgo.schemas.data_source import DataSourceBase


class FeatureSetBase(BaseModel):
    id: int


class FeatureSetCreate(BaseModel):
    snowflakeTable: str
    name: str
    dataSource: DataSourceBase
    granularity: Optional[str]


class FeatureSet(FeatureSetBase):
    name: str
    granularity: Optional[str]
