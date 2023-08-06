class AttributeDefinition(dict):
    """
    Class of db attribute definition
    """

    def __init__(self, name, attribute_type):
        self.AttributeName: str = name
        self.AttributeType: str = attribute_type
        dict.__init__(self, **self.__dict__)
