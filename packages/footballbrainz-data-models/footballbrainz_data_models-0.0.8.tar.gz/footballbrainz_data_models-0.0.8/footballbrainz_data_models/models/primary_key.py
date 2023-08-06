class PrimaryKey(dict):
    """
    Class of db primary key
    """

    def __init__(self, name):
        self.name: str = name
        dict.__init__(self, **self.__dict__)
