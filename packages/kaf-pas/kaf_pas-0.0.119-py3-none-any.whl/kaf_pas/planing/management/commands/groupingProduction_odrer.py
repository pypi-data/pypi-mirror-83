import logging

from django.core.management import BaseCommand
from django.db import transaction

from kaf_pas.planing.models.production_order import Production_orderManager

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            # Production_orderManager.fullRows(f'_user_id_2')
            Production_orderManager.grouping(location_id=117, level_grouping=1)

            # query = Production_order.objects.filter(props=Production_order.props.for_grouping)
            # list2d = map(lambda x: x.location_ids, query)
            # merged = list(set(itertools.chain(*list2d)))

            # query = Production_order.objects.filter(location_ids=[117], props=Production_order.props.for_grouping)
            # pbar = tqdm(total=query.count())
            # for production_order in query:
            #     Production_orderManager.update_redundant_planing_production_order_table(production_order.id)
            #     pbar.update()
            # pbar.close()
