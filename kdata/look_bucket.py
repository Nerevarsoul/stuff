#!/home/neri/.virtualenvs/kdata/bin/python

import boto
import boto.s3.connection


access_key = 'secret'
secret_key = 'secret'
my_folder = 'imagetm'
bucket_name = "marks"


conn = boto.connect_s3(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    host='objects.dreamhost.com',
    calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )

bucket = conn.get_bucket(bucket_name)

for key in bucket.list():
    print(key.name)
