class PrimaryKey(dict):
    """
    Class of db primary key
    """

    def __init__(self, name, key_type="HASH"):
        self.AttributeName: str = name
        self.KeyType: str = key_type
        dict.__init__(self, **self.__dict__)
