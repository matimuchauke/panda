import logging
from typing import List, Union

from pydantic import ValidationError

from panda.apps.transactions.ingestion.models import Transaction
from panda.utils.ingestion import Validator

logger = logging.getLogger(__name__)


class CsvRowValidator(Validator):
    headings = ["Date", "Purchase/Sale", "Country", "Currency", "Net", "VAT"]

    def validate(self, row: List) -> Union[Transaction, bool]:
        if not self.valid_cell_length(row):
            logger.debug("Invalid cells length : %s", len(row))
            return False
        try:
            return Transaction(
                date=row[0],
                transaction_type=row[1],
                country=row[2],
                currency=row[3],
                net=row[4],
                vat=row[5],
            )
        except ValidationError as e:
            logger.debug(e.errors())
            return False

    def valid_cell_length(self, row: List):
        return len(row) == len(self.headings)
