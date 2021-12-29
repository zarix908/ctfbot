class DictMixin:
    def dict(self):
        res = {}

        for column in self.__table__.columns:
            res[column.name] = self.__dict__[column.name]

        return res
