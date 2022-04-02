import json
import logging
from pathlib import Path

from app.models import Quote
from app.serializers import QuoteSerializer
from django.core.management.base import BaseCommand
from django.db import transaction

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Command(BaseCommand):
    # * here I told flake8 to ignore shadowing builtin attribute help
    # * because name help defined by django lib

    help = "add dataset of vehicles models into db, max rows is 10000"  # noqa: VNE003, A003

    DEFAULT_LIMIT = 100000000
    DEFAULT_DIR = (
        Path(__file__)
        .resolve()
        .parent.joinpath("new_motivational_quotes_dataset.json")
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit", type=int, default=self.DEFAULT_LIMIT
        )
        parser.add_argument(
            "--path", type=str, default=self.DEFAULT_DIR
        )

    def _clean_the_table(self):
        Quote.objects.all().delete()

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            logger.info(
                "sript was started, previous Quote table will be erased"
            )
            self._clean_the_table()

            path_to_json_file = Path(kwargs["path"])
            models_number = int(kwargs["limit"])

            logger.debug(f"{models_number=}")
            logger.debug(f"{path_to_json_file=}")

            quotes = None
            with open(path_to_json_file, "r") as f:
                quotes = json.load(f)

            quotes = quotes[:models_number]

            quotes_length = len(quotes)
            logger.debug(f"storring first {quotes_length} models")

            serializer = QuoteSerializer(data=quotes, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            logger.info(
                "all quotes was successfully stored to the DataBase"
            )
