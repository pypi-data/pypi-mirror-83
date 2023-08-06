from typing import Optional
from pydantic import BaseModel
from pyrasgo.schemas.dimensionality import Dimensionality
from pyrasgo.schemas.feature_set import FeatureSetBase


class ColumnCreate(BaseModel):
    name: str
    dataType: str
    featureSet: FeatureSetBase
    dimensionality: Dimensionality

class ColumnUpdate(BaseModel):
    id: int
    name: Optional[str]
    dataType: Optional[str]
    featureSet: Optional[FeatureSetBase]
    dimensionality: Optional[Dimensionality]

class Column(BaseModel):
    id: Optional[int]


