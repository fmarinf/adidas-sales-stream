import boto3
import pandas as pd
import json
from datetime import datetime
import uuid
import pytz

tz_date = pytz.timezone('America/Santiago')

df = pd.read_csv("sales-adidas.csv", sep = ";")

nombre_stream = 'sales-adidas'

#Creamos el cliente de Kinesis
kinesis = boto3.client('kinesis')

for index, row in df.iterrows():
  datetime_scl = datetime.now(tz_date)
  record = {
    'reg_id': str(uuid.uuid4()), #creating random id
    'gen_date': datetime_scl.strftime("%Y-%m-%d %H:%M:%S"),
    'city': row['City'],
    'price': row['Price per Unit'],
    'quantity': row ['Units Sold'],
    'method': row['Sales Method']
  }
  
  print(record)
  
  kinesis.put_record(
    StreamName = nombre_stream,
    Data = json.dumps(record),
    PartitionKey = str(uuid.uuid4())
  )
