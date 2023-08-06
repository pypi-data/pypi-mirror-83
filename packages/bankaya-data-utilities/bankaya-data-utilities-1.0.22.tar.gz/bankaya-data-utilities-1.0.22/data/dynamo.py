from .util import get_data_yaml_dict, get_dynamo_table, replace_decimals
from .cdc_parser import CDCParser
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from datetime import datetime
import json
import logging

cdc_connection = 'cdc'


class Dynamo:

    connections = None

    @classmethod
    def initialize_connections(cls, environment=None):
        try:
            if environment is None:
                Dynamo.connections = get_data_yaml_dict(cls.__name__.lower())
            else:
                Dynamo.connections = get_data_yaml_dict(cls.__name__.lower(), environment)
        except Exception as e:
            logging.exception("exception thrown in Dynamo.initialize_connections")

    def get_cdc_data(self, customer_id):
        try:
            logging.info(f'Dynamo.get_cdc_data with customer_id {customer_id}')
            c = Dynamo.connections[cdc_connection]
            return self.get_item_by_last_date(cdc_connection, c['cdc_dynamo_table'], c['cdc_customer_id_attr'],
                                              customer_id, c['cdc_date_attr'])
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_cdc_data")
            return None

    def get_cdc_features(self, customer_id):
        try:
            logging.info(f'Dynamo.get_cdc_features with customer_id {customer_id}')
            c = Dynamo.connections[cdc_connection]
            item = self.get_cdc_data(customer_id)
            return {'data': item, 'features': CDCParser(item[c['cdc_json_attr']]).get_features()} \
                if item is not None and 'cdc_json_attr' in c and c['cdc_json_attr'] in item else None
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_cdc_features")
            return None

    def insert(self, connection, table, data_dict):
        try:
            logging.info(f'Dynamo.insert with connection {connection} and table {table} and data_dict {data_dict}')
            c = Dynamo.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            dynamo_table.put_item(Item=json.loads(json.dumps(data_dict), parse_float=Decimal))
            return True
        except Exception as e:
            logging.exception("exception thrown in Dynamo.insert")
            return False

    def get_items_by_key(self, connection, table, pk_attr, pk_value):
        try:
            logging.info(f'Dynamo.get_items_by_key with connection {connection} and table {table} and pk_attr {pk_attr} and pk_value {pk_value}')
            c = Dynamo.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            return replace_decimals(dynamo_table.query(KeyConditionExpression=Key(pk_attr).eq(pk_value))['Items'])
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_items_by_key")
            return None

    def get_item_by_pk(self, connection, table, pk_attr, pk_value):
        try:
            logging.info(f'Dynamo.get_item_by_pk with connection {connection} and table {table} and pk_attr {pk_attr} and pk_value {pk_value}')
            c = Dynamo.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            return replace_decimals(dynamo_table.get_item(Key={pk_attr: pk_value})['Item'])
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_item_by_pk")
            return None

    def get_items(self, connection, table, attr, value):
        try:
            logging.info(f'Dybamo.get_items with connection {connection} and table {table} and attr {attr} and value {value}')
            c = Dynamo.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            return replace_decimals(dynamo_table.scan(FilterExpression=Attr(attr).eq(value))['Items'])
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_items")
            return None

    def get_item(self, connection, table, attr, value):
        try:
            logging.info(f'Dybamo.get_item with connection {connection} and table {table} and attr {attr} and value {value}')
            return self.get_items(connection, table, attr, value)[0]
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_item")
            return None

    def get_item_by_key_and_last_date(self, connection, table, pk_attr, pk_value, date_attr):
        try:
            logging.info(f'Dybamo.get_item_by_key_and_last_date with connection {connection} and table {table} and pk_attr {pk_attr} and value {pk_value} and date_attr {date_attr}')
            c = Dynamo.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            items = replace_decimals(dynamo_table.query(KeyConditionExpression=Key(pk_attr).eq(pk_value))['Items'])
            if len(items) > 0:
                items = sorted(items, key=lambda x: datetime.strptime(x[date_attr], '%Y-%m-%dT%H:%M:%S.%fZ'))
                return items[-1]
            else:
                return None
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_item_by_key_and_last_date")
            return None


    def get_item_by_last_date(self, connection, table, attr, value, date_attr):
        try:
            logging.info(f'Dybamo.get_item_by_last_date with connection {connection} and table {table} and attr {attr} and value {value} and date_attr {date_attr}')
            c = Dynamo.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            items = replace_decimals(dynamo_table.scan(FilterExpression=Attr(attr).eq(value))['Items'])
            if len(items) > 0:
                items = sorted(items, key=lambda x: datetime.strptime(x[date_attr], '%Y-%m-%dT%H:%M:%S.%fZ'))
                return items[-1]
            else:
                return None
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_item_by_last_date")
            return None


