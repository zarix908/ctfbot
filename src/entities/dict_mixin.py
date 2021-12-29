class DictMixin:
    def dict(self):
        res = {}

        for column in self.__table__.columns:
            res[column.name] = getattr(self, column.name)

        return res
