import boto3
from boto3.dynamodb.conditions import Key, Attr
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker


class S3():
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region="us-east-1"):
        self.s3 = boto3.resource(
            's3', 
            region_name=region, 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key
        )

    def get_object(self, p_bucket, p_key):
        try:
            obj = self.s3.Object(p_bucket, p_key)
            data = obj.get()["Body"].read().decode("utf-8")
            return data
        except Exception as error:
            return str(error)

    def get_object_as_object(self, p_bucket, p_key):
        try:
            obj = self.s3.Object(p_bucket, p_key)
            data = obj.get()["Body"]
            return data
        except Exception as error:
            return str(error)

    def put_object(self, p_bucket, p_key, p_file):
        try:
            bucket = self.s3.Bucket(p_bucket)
            bucket.put_object(Bucket=p_bucket, Key=p_key, Body=p_file)
            return  'Success'
        except Exception as error:
            return str(error)

    def delete_object(self, p_bucket, p_key):
        try:
            obj = self.s3.Object(p_bucket, p_key)
            obj.delete()
            return 'Success'
        except Exception as error:
            return str(error)

    def exist_object(self, p_bucket, p_key):
        try:
            bucket = self.s3.Bucket(p_bucket)
            objs = list(bucket.objects.filter(Prefix=p_key))
            if len(objs) > 0 and objs[0].key == p_key:
                return True
            else:
                return False
        except Exception as error:
            return str(error)

    def list_all_objects(self, p_bucket):
        try:
            l_file_bk = list()
            bucket = self.s3.Bucket(p_bucket)
            for i in bucket.objects.all():
                l_file_bk.append(i.key)
            return l_file_bk
        except Exception as error:
            return str(error)

    def list_path_objects(self, p_bucket, p_path):
        try:
            l_file_bk = list()
            bucket = self.s3.Bucket(p_bucket)
            for obj in list(bucket.objects.filter(Prefix=p_path)):
                l_file_bk.append(obj.key)
            return l_file_bk
        except Exception as error:
            return str(error)

    def list_like_objects(self, p_bucket, p_like):
        try:
            l_file_bk = list()
            bucket = self.s3.Bucket(p_bucket)
            for i in bucket.objects.all():
                if p_like in i.key:
                    l_file_bk.append(i.key)
            return l_file_bk
        except Exception as error:
            return str(error)

    def copy_object_another_bucket(self, p_bucket_ori, p_key_ori, p_bucket_dest, p_key_dest):
        try:
            copy_source = {'Bucket': p_bucket_ori
                         , 'Key': p_key_ori}
            bucket = self.s3.Bucket(p_bucket_dest)
            bucket.copy(copy_source, p_key_dest)
            return 'Success'
        except Exception as error:
            return str(error)
    

class SQS():
    
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region="us-east-1"):
        self.sqs = boto3.client(
            'sqs', 
            region_name=region,
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key
        )

    def get_item_queue(self, queue_name, account_id):
        try:
            url = self.sqs.get_queue_url(
                QueueName = queue_name,
                QueueOwnerAWSAccountId = account_id
            )

            if url['QueueUrl']:
                response = self.sqs.receive_message(
                    QueueUrl=url['QueueUrl'],
                    AttributeNames=[
                        'SentTimestamp'
                    ],
                    MaxNumberOfMessages=1,
                    MessageAttributeNames=[
                        'All'
                    ],
                    VisibilityTimeout=0,
                    WaitTimeSeconds=0
                )

                if 'Messages' in response:
                    message = response['Messages'][0]
                    receipt_handle = message['ReceiptHandle']

                
                    self.sqs.delete_message(
                        QueueUrl=url['QueueUrl'],
                        ReceiptHandle=receipt_handle
                    )

                    return message
            return None
        except Exception as error:
            return str(error)


class DynamoDb():
    
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region="us-east-1"):
        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key =aws_secret_access_key, 
            region_name=region
        )

    def create_table(self, create):
        try:
            self.table = self.dynamodb.create_table(
                TableName=create['TableName'], 
                KeySchema=[
                    {'AttributeName': create['AttPk'], 'KeyType': create['KTypePk']},
                    {'AttributeName': create['AttSk'], 'KeyType': create['KTypeSk']}
                ], 
                AttributeDefinitions=[
                    {'AttributeName': create['AttPk'], 'AttributeType': create['TypePk']},
                    {'AttributeName': create['AttSk'], 'AttributeType': create['TypeSk']}, 
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': create['ReadCap'],
                    'WriteCapacityUnits': create['WriteCap']
                }
            )
            return 'Success'
        except Exception as error:
            return str(error)

    def drop_table(self, table_name):
        try:
            self.table = self.dynamodb.Table(table_name)
            self.table.delete()
            return 'Success'
        except Exception as error:
            return str(error)

    def post_table(self, table, item):
        try:
            self.table = self.dynamodb.Table(table)
            self.table.put_item(Item=item)
            return 'Success'
        except Exception as error:
            return str(error)

    def put_table(self, table, key, set_expression, value, attr):
        try:
            self.table = self.dynamodb.Table(table)
            self.table.update_item(
                Key=key,
                UpdateExpression=set_expression,
                ExpressionAttributeValues=value,
                ExpressionAttributeNames=attr,
                ReturnValues="ALL_NEW"
            )
            return 'Success'
        except Exception as error:
            return str(error)

    def delete_table(self, table, key):
        try:
            self.table = self.dynamodb.Table(table)
            self.table.delete_item(Key=key)
            return 'Success'
        except Exception as error:
            return str(error)

    def scan_table(self, table):
        try:
            self.table = self.dynamodb.Table(table)
            response = self.table.scan()
            return response['Items']
        except Exception as error:
            return str(error)

    def get_item_by_key(self, table, key):
        try:
            self.table = self.dynamodb.Table(table)
            response = self.table.get_item(Key=key)
            return response['Item']
        except Exception as error:
            return str(error)


class Redshift():
    
    def __init__(self, user, password, host, port, database):
        self.connection = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.connection)

    def get_engine(self):
        return self.engine

    def create_session(self):
        try:
            self.Session = sessionmaker(self.engine)
            self.session = self.Session()
            return self.session
        except Exception as error:
            return str(error)

    def close_session(self):
        try:
            self.session.close()
            return 'Session closed'
        except Exception as error:
            return str(error)