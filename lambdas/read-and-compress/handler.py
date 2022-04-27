import boto3
from io import BytesIO
import zipfile

s3 = boto3.resource('s3')

def handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        split = key.split(".")
        file_name = split[0]
        complete_file_name = '{}.zip'.format(file_name)

## ZIP FILE WITH PYTHON ZIP PACKAGE ###
        file = s3.Object(bucket,key)
        body = file.get()['Body'].read()
        archive = BytesIO()
        print('archive => ', archive)
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
            print('inside zip_archive')
            with zip_archive.open(file.key, 'w') as file1:
                print('inside file1')
                file1.write(body)
                print('Wroted and closed')  

        print('Upload file to s3.')
        archive.seek(0)
        s3.Object('after-compress-files',complete_file_name).upload_fileobj(archive)
        archive.close()
## ZIP FILE WITH PYTHON ZIP PACKAGE ###
    except Exception as e:
        print('Error handler() => ', e)