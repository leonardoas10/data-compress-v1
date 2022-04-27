import boto3
from datetime import datetime
import json
import os

s3 = boto3.client('s3')

def handler(event, context):
    try:
        init_time = datetime.now()
        print('Init Lambda => ', init_time)

        # temp_url = s3.generate_presigned_url(
        #     ClientMethod='put_object',
        #     Params={
        #         'Bucket': 'before-compress-files',
        #         'Key': 'leo.txt',
        #     }
        # )

        # # Upload a file named 'test.txt' using cURL
        # os.system('curl --request PUT --upload-file ./leo.txt "' + temp_url + '"')

        urls = dict()
        data = json.loads(event['body'])
        print(data)
        for index, file in enumerate(data['files']):
            # key = "uploads/{}".format(file['path'])
            presigned_url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': 'before-compress-files',
                    'Key': file['path'],
                    'ContentType' : data['types'][index]
                }
            )
            urls[file['path']] = presigned_url

          
        duration = datetime.now() - init_time
        print('Finish Time in seconds => ', duration.total_seconds())
        print(urls)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(urls),
        }
    except Exception as e:
        print('Error => ', e)
