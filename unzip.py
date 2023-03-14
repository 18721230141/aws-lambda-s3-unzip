import json
import urllib.parse
import boto3
import io
import zipfile
import os

print('Loading function')

s3 = boto3.client('s3')

bucket = 'your buckets name'

def lambda_handler(event, context):
    #key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        putObjects = []
        with io.BytesIO(obj["Body"].read()) as tf:
            # rewind the file
            tf.seek(0)

            # Read the file as a zipfile and process the members
            with zipfile.ZipFile(tf, mode='r') as zipf:
                dirpath = os.path.dirname(key) + "/"
                print(dirpath)
                for file in zipf.infolist():
                    fileName = file.filename
                    print(fileName)
                    filepath = dirpath + fileName
                    putFile = s3.put_object(ACL = 'public-read', Bucket=bucket, Key = filepath, Body = zipf.read(file))
                    putObjects.append(putFile)
                    print(putFile)
                    
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e    
