import os
import sys
import yaml
import json
import boto3
import decimal

data_yaml_file = '/data'
extension = '.yml'


def get_data_yaml_dict(connection_type, environment=None):
    try:
        sFile = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        sFile = sys.executable
    file_name = data_yaml_file + extension if environment is None else data_yaml_file + '_' + environment + extension
    return yaml.load(open(os.path.dirname(sFile) + file_name), Loader=yaml.FullLoader)[connection_type]


def get_log_file_path(file_name):
    try:
        sFile = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        sFile = sys.executable
    return os.path.dirname(sFile) + '/' + file_name


def get_dynamo_table(access_key, secret_access_key, region, table):
    return boto3.resource('dynamodb',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_access_key,
                          region_name=region).Table(table)


def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
