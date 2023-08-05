import datetime
from botocore.exceptions import ClientError
from amazon_web_services_helpers.aws_helper import AwsHelper


class DocumentStore:
    def __init__(self, documents_table_name, output_table_name):
        self._documentsTableName = documents_table_name
        self._outputTableName = output_table_name

    def create_document(self, document_id, bucket_name, object_name):
        err = None
        dynamodb = AwsHelper().get_resource("dynamodb")
        table = dynamodb.Table(self._documentsTableName)
        try:
            table.update_item(
                Key={"documentId": document_id},
                UpdateExpression='SET bucketName = :bucketNameValue, objectName = :objectNameValue, documentStatus = :documentstatusValue, documentCreatedOn = :documentCreatedOnValue',
                ConditionExpression='attribute_not_exists(documentId)',
                ExpressionAttributeValues={
                    ':bucketNameValue': bucket_name,
                    ':objectNameValue': object_name,
                    ':documentstatusValue': 'IN_PROGRESS',
                    ':documentCreatedOnValue': str(datetime.datetime.utcnow())
                }
            )
        except ClientError as e:
            print(e)
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
                err = {'Error': 'Document already exist.'}
            else:
                raise

        return err

    def update_document_status(self, document_id, document_status):
        err = None
        dynamodb = AwsHelper().get_resource("dynamodb")
        table = dynamodb.Table(self._documentsTableName)
        try:
            table.update_item(
                Key={'documentId': document_id},
                UpdateExpression='SET documentStatus= :documentstatusValue',
                ConditionExpression='attribute_exists(documentId)',
                ExpressionAttributeValues={
                    ':documentstatusValue': document_status
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
                err = {'Error': 'Document does not exist.'}
            else:
                raise

        return err

    def mark_document_complete(self, document_id):
        err = None
        dynamodb = AwsHelper().get_resource("dynamodb")
        table = dynamodb.Table(self._documentsTableName)
        try:
            table.update_item(
                Key={'documentId': document_id},
                UpdateExpression='SET documentStatus= :documentstatusValue, documentCompletedOn = :documentCompletedOnValue',
                ConditionExpression='attribute_exists(documentId)',
                ExpressionAttributeValues={
                    ':documentstatusValue': "SUCCEEDED",
                    ':documentCompletedOnValue': str(datetime.datetime.utcnow())
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
                err = {'Error': 'Document does not exist.'}
            else:
                raise
        return err

    def get_document(self, document_id):
        dynamodb = AwsHelper().get_client("dynamodb")
        ddb_get_item_response = dynamodb.get_item(
            Key={'documentId': {'S': document_id}},
            TableName=self._documentsTableName
        )
        item_to_return = None
        if 'Item' in ddb_get_item_response:
            item_to_return = {
                'documentId': ddb_get_item_response['Item']['documentId']['S'],
                'bucketName': ddb_get_item_response['Item']['bucketName']['S'],
                'objectName': ddb_get_item_response['Item']['objectName']['S'],
                'documentStatus': ddb_get_item_response['Item']['documentStatus']['S']
            }
        return item_to_return

    def delete_document(self, documentId):
        dynamodb = AwsHelper().get_resource("dynamodb")
        table = dynamodb.Table(self._documentsTableName)
        table.delete_item(
            Key={
                'documentId': documentId
            }
        )

    def get_documents(self, next_token=None):
        dynamodb = AwsHelper().get_resource("dynamodb")
        table = dynamodb.Table(self._documentsTableName)
        page_size = 25
        if next_token:
            response = table.scan(ExclusiveStartKey={"documentId": next_token}, Limit=page_size)
        else:
            response = table.scan(Limit=page_size)
        print("response: {}".format(response))
        data = []
        if 'Items' in response:
            data = response['Items']
        documents = {
            "documents": data
        }
        if 'LastEvaluatedKey' in response:
            next_token = response['LastEvaluatedKey']['documentId']
            print("nexToken: {}".format(next_token))
            documents["nextToken"] = next_token
        return documents
