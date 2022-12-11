import csv
import logging
from io import StringIO

from panda.apps.transactions.ingestion import Transaction
from panda.utils.ingestion import Transformer
import requests

logger = logging.getLogger(__name__)


class CsvRowTransformer(Transformer):
    START_DATE = "2020-01-01"
    END_DATE = "2020-12-31"
    BASE_CURRENCY = "EUR"
    BASE_URL = f'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D..{BASE_CURRENCY}.SP00.A'

    def __init__(self):
        self.lookup = {}
        url = f"{self.BASE_URL}/?startPeriod={self.START_DATE}&endPeriod={self.END_DATE}&format=csvdata"
        rates_csv = StringIO(requests.get(url).text)
        rates = csv.reader(rates_csv, delimiter=',')
        for record in rates:
            currency, day, rate = record[2], record[6], record[7]
            logger.info("Exchange Rate %s to %s for day %s", self.BASE_CURRENCY, currency, day)
            self.lookup.update({f"{day}-{currency}": rate})

    def transform(self, row: Transaction) -> Transaction:
        exchange_rate = self.get_rate(row)
        if exchange_rate:
            return row.copy(update={
                "currency": self.BASE_CURRENCY,
                "net": round(row.net / exchange_rate, 2),
                "vat": round(row.vat / exchange_rate, 2)
            })
        return row

    def get_rate(self, row: Transaction):
        value = self.lookup.get(f"{row.date.strftime('%Y-%m-%d')}-{row.currency}")
        if value:
            return float(value)
        return None
