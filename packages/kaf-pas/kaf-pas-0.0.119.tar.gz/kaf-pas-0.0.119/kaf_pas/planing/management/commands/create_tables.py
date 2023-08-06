import logging

from django.core.management import BaseCommand

from isc_common.common.mat_views import create_table, create_insert_update_delete_function_of_table

logger = logging.getLogger(__name__)


def create_production_order_tmp_tables():
    tablenames = ['planing_production_order']

    for tablename in tablenames:
        table_name_tbl = f'''{tablename}_tbl'''
        print(f'Creating: {table_name_tbl}')

        create_table(
            sql_str=f'''select * from {tablename}_view''',
            table_name=table_name_tbl,
            primary_key=[
                'id',
                'item_id',
                'launch_id',
                'location_ids',
                'parent_item_id',
            ],
            indexes=[
                'id',
                'date',
                'item_id',
                'launch_id',
                'parent_item_id',
                'num',
                'isDeleted',
                'opertype_id',
                'props',
                'status_id',
            ]
        )
        print(f'Created: {table_name_tbl}')
        print(f'Creating insert_update_delete_function_of_table: {table_name_tbl}')

        create_insert_update_delete_function_of_table(table_name=tablename, exclude_fields=['parent_item_id', 'parent_item_ids', 'isFolder', 'props'])
        print(f'Created insert_update_delete_function_of_table: {table_name_tbl}')

    tablenames = ['planing_production_order_per_launch']

    for tablename in tablenames:
        table_name_tbl = f'''{tablename}_tbl'''
        print(f'Creating: {table_name_tbl}')

        create_table(
            sql_str=f'''select * from {tablename}_view''',
            table_name=table_name_tbl,
            primary_key=[
                'id',
                'item_id',
                'launch_id',
                'location_ids',
                'parent_item_id',
            ],
            indexes=[
                'id',
                'date',
                'item_id',
                'launch_id',
                'parent_item_id',
                'num',
                'opertype_id',
                'props',
                'status_id',
            ]
        )

        print(f'Created: {table_name_tbl}')
        print(f'Creating insert_update_delete_function_of_table: {table_name_tbl}')

        create_insert_update_delete_function_of_table(
            table_name=tablename,
            func_params=[('id', 'bigint'), ('launch_id', 'bigint')],
            exclude_fields=['parent_item_id', 'parent_item_ids', 'isFolder', 'props']
        )

        print(f'Created insert_update_delete_function_of_table: {table_name_tbl}')


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_production_order_tmp_tables()

        from kaf_pas.planing.models.production_order import Production_order
        from isc_common.common import doing
        ids = list(map(lambda x: x.id, Production_order.objects.exclude(status__code=doing)))
        print(f'check_state: Production_order')
        Production_order.objects.filter(id__in=ids).check_state()

        print(f'check_state: Production_order_per_launch')
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        ids = list(map(lambda x: x.id, Production_order_per_launch.objects.exclude(status__code=doing)))
        Production_order_per_launch.objects.filter(id__in=ids).check_state()
