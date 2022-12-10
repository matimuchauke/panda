from typing import Iterable

from panda.apps.transactions.ingestion import CsvRowValidator, CsvRowTransformer, CsvLoader
from panda.utils.ingestion import CsvExtractor, IngestionProcess


class CsvIngestionProcess(IngestionProcess):

    def __init__(self, csv_file: str):
        """ TODO : Use Dependency Injection """
        self.extractor = CsvExtractor(csv_file, delimiter=',')
        self.validator = CsvRowValidator()
        self.transformer = CsvRowTransformer()
        self.loader = CsvLoader()

    def prepare(self, dataset: Iterable) -> Iterable:
        next(dataset, None)  # skip csv headers
        return dataset

    def start(self):
        super().start()
