import logging

from django.core.management import BaseCommand
from django.db import transaction

from kaf_pas.planing.models.production_order import Production_orderManager

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            Production_orderManager.ungrouping(location_id=117, users=Production_orderManager.get_use_4_grouping_message(location_id=117))
