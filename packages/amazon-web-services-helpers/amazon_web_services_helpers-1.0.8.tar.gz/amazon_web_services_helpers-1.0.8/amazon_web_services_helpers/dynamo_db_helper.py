from boto3.dynamodb.conditions import Key
from amazon_web_services_helpers.aws_helper import AwsHelper


class DynamoDbHelper:
    @staticmethod
    def get_items(table_name, key, value, index_name=None):
        items = None
        ddb = AwsHelper().get_resource("dynamodb")
        table = ddb.Table(table_name)
        if key is not None and value is not None:
            filter = Key(key).eq(value)
            query_result = None
            if index_name:
                query_result = table.query(IndexName=index_name, KeyConditionExpression=filter)
            else:
                query_result = table.query(KeyConditionExpression=filter)
            if query_result and "Items" in query_result:
                items = query_result["Items"]
        return items

    @staticmethod
    def insert_item(table_name, item_data):
        ddb = AwsHelper().get_resource("dynamodb")
        table = ddb.Table(table_name)
        ddb_response = table.put_item(Item=item_data)
        return ddb_response

    @staticmethod
    def delete_items(table_name, key, value, sk):
        items = DynamoDbHelper.get_items(table_name, key, value)
        if items:
            ddb = AwsHelper().get_resource("dynamodb")
            table = ddb.Table(table_name)
            for item in items:
                print("Deleting...")
                print("{} : {}".format(key, item[key]))
                print("{} : {}".format(sk, item[sk]))
                table.delete_item(
                    Key={
                        key: value,
                        sk: item[sk]
                    })
                print("Deleted...")