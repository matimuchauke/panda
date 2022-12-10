from panda.apps.transactions.ingestion import Transaction
from panda.utils.ingestion import Transformer


class CsvRowTransformer(Transformer):

    def transform(self, row: Transaction) -> Transaction:
        return row
