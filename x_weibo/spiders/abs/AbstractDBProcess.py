import abc


class AbstractDBProcess(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def process_item(self, items, spider):
        pass

    @abc.abstractmethod
    def close_spider(self, spider):
        pass
