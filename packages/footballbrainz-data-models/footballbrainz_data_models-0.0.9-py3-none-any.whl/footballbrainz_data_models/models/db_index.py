from typing import List
from footballbrainz_data_models.models.primary_key import PrimaryKey
from footballbrainz_data_models.models.attribute_projection import AttributeProjection


class DbIndex(dict):
    """
    Class of db index definition
    """

    def __init__(self, name, primary_key, projection=None):
        self.name: str = name
        self.primary_key: PrimaryKey = primary_key
        self.Projection: AttributeProjection = projection
        dict.__init__(self, **self.__dict__)
