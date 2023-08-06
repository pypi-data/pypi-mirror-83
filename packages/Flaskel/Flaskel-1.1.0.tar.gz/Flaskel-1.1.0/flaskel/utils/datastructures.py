class HashableDict(dict):
    def __hash__(self):
        """

        :return:
        """
        return hash(tuple(sorted(self.items())))
