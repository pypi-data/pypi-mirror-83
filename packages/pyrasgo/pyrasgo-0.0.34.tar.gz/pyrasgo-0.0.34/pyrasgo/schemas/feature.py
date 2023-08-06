from typing import List, Optional
from pydantic import BaseModel

from pyrasgo.schemas.data_source import DataSource
from pyrasgo.schemas.feature_set import FeatureSet
from pyrasgo.schemas.granularity import Granularity


class FeatureBase(BaseModel):
    id: int


class FeatureCreate(BaseModel):
    name: str
    code: Optional[str]
    description: Optional[str]
    columnId: Optional[int]
    featureSetId: Optional[int]
    organizationId: Optional[int]
    orchestrationStatus: Optional[str]
    tags: Optional[List[str]]

class FeatureUpdate(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    #Can't include these until we create a v1 patch endpoint for features
    #columnId: Optional[int]
    #featureSetId: Optional[int]
    #organizationId: Optional[int]
    #orchestrationStatus: Optional[str]
    #tags: Optional[List[str]]

class Feature(FeatureBase):
    id: str  # TODO: Returning feature ids as strings, ensure consistency.
    name: str
    description: Optional[str]
    code: Optional[str]
    columnId: Optional[int]
    dataType: Optional[str]
    dataSource: Optional[DataSource]
    featureSet: Optional[FeatureSet]
    granularities: Optional[List[Granularity]]
    orchestrationStatus: Optional[str]
    tags: Optional[List[str]]
