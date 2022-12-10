import csv
import logging
from abc import abstractmethod
from typing import Protocol, Iterable, Any

logger = logging.getLogger(__name__)


class Extractor(Protocol):
    @abstractmethod
    def extract(self, *args, **kwargs) -> Iterable:
        pass


class CsvExtractor(Extractor):
    def __init__(self, csv_file: str, **kwargs):
        self.csv_file = csv_file
        self.kwargs = kwargs

    def extract(self) -> Iterable:
        file = open(self.csv_file, newline='')  # TODO : make sure the file get closed
        return csv.reader(file, **self.kwargs)


class Validator(Protocol):
    @abstractmethod
    def validate(self, data: Any) -> Any:
        pass


class Transformer(Protocol):
    @abstractmethod
    def transform(self, data: Any) -> Any:
        pass


class Loader(Protocol):
    dataset: Any = None

    @abstractmethod
    def insert(self, data: Any):
        pass

    @abstractmethod
    def load(self):
        pass


class IngestionProcess(Protocol):
    extractor: Extractor = None
    validator: Validator = None
    transformer: Transformer = None
    loader: Loader = None

    def start(self):
        dataset = self.prepare(self.extractor.extract())
        for data in dataset:
            if validated := self.validator.validate(data):
                self.loader.insert(self.transformer.transform(validated))
        self.loader.load()

    @abstractmethod
    def prepare(self, dataset: Iterable) -> Iterable:
        pass

