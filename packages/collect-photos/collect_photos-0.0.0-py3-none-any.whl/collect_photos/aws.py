import boto3

from collect_photos.mounting import Mounting

table_name = 'Lambda-Halftoning-Photo'
bucket_name = 'mwenclubhouse-halftoning-project'

aws_access_key_id = "AKIAZTPFGCYMATPM3G6N"
aws_secret_access_key = "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"
region_name = "us-east-2"


class AwsTasks:

    def __init__(self):
        pass

    @staticmethod
    def get_dynamodb_client(client):
        return boto3.client("dynamodb") if client is None else client

    @staticmethod
    def get_s3_resource(resource):
        return boto3.resource('s3') if resource is None else resource

    @staticmethod
    def __parse_file(list_response):
        list_dict = []
        for item in list_response:
            list_dict.append({
                "uploaded": item["uploaded"]['BOOL'],
                "name": item["name"]["S"]
            })
        return list_dict

    @staticmethod
    def log_file(file_name, is_uploaded=False, client=None):
        client = AwsTasks.get_dynamodb_client(client)
        try:
            file_from_db = AwsTasks.query_file(file_name)
            if file_from_db is None or (file_from_db["uploaded"] is False):
                client.put_item(
                    TableName=table_name,
                    Item={
                        'name': {
                            'S': file_name
                        },
                        'uploaded': {
                            'BOOL': is_uploaded
                        }
                    }
                )
        except Exception as ex:
            if type(ex).__name__ == 'KeyboardException':
                exit(0)
            print("Error Query for File {}".format(file_name))

    @staticmethod
    def query_file(file_name, client=None):
        client = AwsTasks.get_dynamodb_client(client)
        try:
            response = client.query(
                TableName=table_name,
                Select="ALL_ATTRIBUTES",
                KeyConditions={
                    'name': {
                        'AttributeValueList': [{
                            'S': file_name
                        }],
                        'ComparisonOperator': 'EQ'
                    }
                }
            )
            if response['Count'] == 1:
                return AwsTasks.__parse_file(response["Items"])[0]
        except Exception as ex:
            if type(ex).__name__ == 'KeyboardException':
                exit(0)
            print("Error Querying {} from Database".format(file_name))
        return None

    @staticmethod
    def scan_missing(client=None):
        client = AwsTasks.get_dynamodb_client(client)
        try:
            response = client.scan(
                TableName=table_name,
                Select="ALL_ATTRIBUTES",
                ScanFilter={
                    'uploaded': {
                        'AttributeValueList': [
                            {
                                'BOOL': False
                            }
                        ],
                        'ComparisonOperator': 'EQ'
                    }
                }
            )
            return AwsTasks.__parse_file(response["Items"])
        except Exception as ex:
            if type(ex).__name__ == 'KeyboardException':
                exit(0)
            print("Error Trying to Scan From Database")
        return None

    @staticmethod
    def upload_file(file_name, mount, s3_resource=None, database_client=None):
        try:
            s3_client = AwsTasks.get_s3_resource(s3_resource)
            s3_client.meta.client.upload_file(mount.working_directory + file_name, bucket_name, file_name)
            AwsTasks.log_file(file_name, client=database_client, is_uploaded=True)
        except Exception as ex:
            if type(ex).__name__ == 'KeyboardException':
                exit(0)
            print("Error Uploading File: {}".format(mount.working_directory + file_name))
