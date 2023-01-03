import boto3
import json
import time

stream_name = 'sales-adidas'
kinesis = boto3.client('kinesis')

response = kinesis.describe_stream(StreamName = stream_name)
shard_id = response['StreamDescription']['Shards'][0]['ShardId']

print(shard_id)

shard_iterator = kinesis.get_shard_iterator(
    StreamName = stream_name,
    ShardId = shard_id,
    ShardIteratorType = 'LATEST' #historical data: sTRIM_HORIZON
)

my_shard_iterator = shard_iterator['ShardIterator']

record_response = kinesis.get_records(
    ShardIterator = my_shard_iterator,
    Limit = 1
)

#Recorre todo lo que contiene el Streams
while 'NextShardIterator' in record_response:
    record_response = kinesis.get_records(
        ShardIterator = record_response['NextShardIterator'],
        Limit = 1
    )
    
    print("ShardIter : " + record_response['NextShardIterator'])
    
    try: 
        print(record_response['Records'][0]['Data'])
    except Exception:
        print("No data available.")
