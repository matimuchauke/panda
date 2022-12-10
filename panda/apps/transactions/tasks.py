from celery import shared_task

from panda.apps.transactions.ingestion.main import CsvIngestionProcess


@shared_task()
def start_ingestion(path):
    ingestion = CsvIngestionProcess(path)
    ingestion.start()
