import csv
import psycopg2
from io import StringIO

from django.conf import settings

from panda.apps.transactions.ingestion.models import Transaction
from panda.utils.ingestion import Loader


class CsvLoader(Loader):
    def __init__(self):
        self.dataset = StringIO()
        self.count = 0
        self.chunk_size = 10000

    def insert(self, row: Transaction):
        csv.writer(self.dataset).writerow(row.dict().values())
        self.count += 1
        if self.count == self.chunk_size:
            self.load()
            self.dataset = StringIO()
            self.count = 0
            self.chunk_size = 10000
            # TODO : Refactoring

    def load(self):
        db_settings = settings.DATABASES.get('default')
        conn = psycopg2.connect(
            dbname=db_settings.get("NAME"),
            user=db_settings.get("USER"),
            password=db_settings.get("PASSWORD"),
            host=db_settings.get("HOST"),
            port=db_settings.get("PORT")
        )
        cur = conn.cursor()
        self.dataset.seek(0)
        cur.copy_from(
            self.dataset, 'transactions_transaction', sep=',',
            columns=('date', 'transaction_type', 'country', 'currency', 'net', 'vat')
        )
        conn.commit()
